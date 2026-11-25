
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def get_late_delivery_percentage():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        query = """
        SELECT
            ROUND(
                100.0 * COUNT(*) FILTER (
                    WHERE order_delivered_customer_date::timestamp >
                          order_estimated_delivery_date::timestamp
                ) / NULLIF(COUNT(*), 0),
                2
            ) AS late_delivery_percentage
        FROM public.orders
        WHERE order_status = 'delivered'
          AND order_delivered_customer_date IS NOT NULL;
        """

        cursor.execute(query)
        result = cursor.fetchone()

        return result[0]

    finally:
        connection.close()


def get_database_columns():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)

        return cursor.fetchall()

    finally:
        connection.close()


def get_business_metrics():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        query = """
        WITH delivered_orders AS (
            SELECT
                order_id,
                order_purchase_timestamp,
                order_delivered_customer_date,
                order_estimated_delivery_date
            FROM public.orders
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NOT NULL
        ),
        freight_per_order AS (
            SELECT
                oi.order_id,
                SUM(oi.freight_value) AS total_freight
            FROM public.order_items oi
            JOIN delivered_orders d
                ON oi.order_id = d.order_id
            GROUP BY oi.order_id
        )
        SELECT
            COUNT(*) AS total_delivered_orders,

            COUNT(*) FILTER (
                WHERE order_delivered_customer_date >
                      order_estimated_delivery_date
            ) AS late_orders,

            ROUND(
                AVG(EXTRACT(EPOCH FROM (
                    order_delivered_customer_date::timestamp -
                    order_purchase_timestamp::timestamp
                )) / 86400)::numeric, 2
            ) AS average_delivery_days,

            (
                SELECT ROUND(AVG(total_freight)::numeric, 2)
                FROM freight_per_order
            ) AS average_freight_per_order,

            (
                SELECT ROUND(AVG(review_score)::numeric, 2)
                FROM public.order_reviews
            ) AS average_review_score

        FROM delivered_orders;
        """

        cursor.execute(query)
        result = cursor.fetchone()

        return {
            "total_delivered_orders": result[0],
            "late_orders": result[1],
            "average_delivery_days": float(result[2]) if result[2] is not None else None,
            "average_freight_per_order": float(result[3]) if result[3] is not None else None,
            "average_review_score": float(result[4]) if result[4] is not None else None
        }

    finally:
        connection.close()


def get_seller_delivery_performance():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        query = """
        WITH seller_orders AS (
            SELECT DISTINCT
                oi.seller_id,
                o.order_id,
                o.order_delivered_customer_date,
                o.order_estimated_delivery_date
            FROM public.order_items oi
            JOIN public.orders o
                ON oi.order_id = o.order_id
            WHERE o.order_status = 'delivered'
              AND o.order_delivered_customer_date IS NOT NULL
        )

        SELECT
            seller_id,
            COUNT(*) AS total_orders,

            COUNT(*) FILTER (
                WHERE order_delivered_customer_date::timestamp >
                      order_estimated_delivery_date::timestamp
            ) AS late_orders,

            ROUND(
                100.0 * COUNT(*) FILTER (
                    WHERE order_delivered_customer_date::timestamp >
                          order_estimated_delivery_date::timestamp
                ) / NULLIF(COUNT(*), 0),
                2
            ) AS late_delivery_percentage

        FROM seller_orders
        GROUP BY seller_id
        HAVING COUNT(*) >= 20
        ORDER BY late_delivery_percentage DESC
        LIMIT 10;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        return [
            {
                "seller_id": row[0],
                "total_orders": row[1],
                "late_orders": row[2],
                "late_delivery_percentage": float(row[3])
            }
            for row in results
        ]

    finally:
        connection.close()


def get_state_delivery_performance():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        query = """
        WITH state_orders AS (
            SELECT DISTINCT
                s.seller_state,
                o.order_id,
                o.order_delivered_customer_date,
                o.order_estimated_delivery_date
            FROM public.orders o
            JOIN public.order_items oi
                ON o.order_id = oi.order_id
            JOIN public.sellers s
                ON oi.seller_id = s.seller_id
            WHERE o.order_status = 'delivered'
              AND o.order_delivered_customer_date IS NOT NULL
        )

        SELECT
            seller_state,
            COUNT(DISTINCT order_id) AS total_orders,

            COUNT(DISTINCT CASE
                WHEN order_delivered_customer_date::timestamp >
                     order_estimated_delivery_date::timestamp
                THEN order_id
            END) AS late_orders,

            ROUND(
                100.0 * COUNT(DISTINCT CASE
                    WHEN order_delivered_customer_date::timestamp >
                         order_estimated_delivery_date::timestamp
                    THEN order_id
                END) / NULLIF(COUNT(DISTINCT order_id), 0),
                2
            ) AS late_delivery_percentage

        FROM state_orders
        GROUP BY seller_state
        HAVING COUNT(DISTINCT order_id) >= 20
        ORDER BY late_delivery_percentage DESC;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        return [
            {
                "seller_state": row[0],
                "total_orders": row[1],
                "late_orders": row[2],
                "late_delivery_percentage": float(row[3])
            }
            for row in results
        ]

    finally:
        connection.close()


def get_customer_review_analysis():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        summary_query = """
        SELECT
            COUNT(*) AS total_reviews,
            ROUND(AVG(review_score)::numeric, 2) AS average_review_score,

            COUNT(*) FILTER (
                WHERE review_score <= 2
            ) AS low_rated_reviews,

            ROUND(
                100.0 * COUNT(*) FILTER (
                    WHERE review_score <= 2
                ) / NULLIF(COUNT(*), 0),
                2
            ) AS low_rating_percentage

        FROM public.order_reviews
        WHERE review_score IS NOT NULL;
        """

        cursor.execute(summary_query)
        summary = cursor.fetchone()

        distribution_query = """
        SELECT
            review_score,
            COUNT(*) AS total_reviews
        FROM public.order_reviews
        WHERE review_score IS NOT NULL
        GROUP BY review_score
        ORDER BY review_score;
        """

        cursor.execute(distribution_query)
        distribution = cursor.fetchall()

        return {
            "total_reviews": summary[0],
            "average_review_score": float(summary[1]),
            "low_rated_reviews": summary[2],
            "low_rating_percentage": float(summary[3]),
            "review_score_distribution": [
                {
                    "review_score": row[0],
                    "total_reviews": row[1]
                }
                for row in distribution
            ]
        }

    finally:
        connection.close()



def get_delivery_review_analysis():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        query = """
        WITH order_delivery_status AS (
            SELECT
                order_id,
                CASE
                    WHEN order_delivered_customer_date::timestamp >
                         order_estimated_delivery_date::timestamp
                    THEN 'Late Delivery'
                    ELSE 'On-Time Delivery'
                END AS delivery_status
            FROM public.orders
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NOT NULL
              AND order_estimated_delivery_date IS NOT NULL
        )

        SELECT
            d.delivery_status,
            COUNT(r.review_id) AS total_reviews,
            ROUND(AVG(r.review_score)::numeric, 2)
                AS average_review_score,

            COUNT(r.review_id) FILTER (
                WHERE r.review_score <= 2
            ) AS low_rated_reviews,

            ROUND(
                100.0 * COUNT(r.review_id) FILTER (
                    WHERE r.review_score <= 2
                ) / NULLIF(COUNT(r.review_id), 0),
                2
            ) AS low_rating_percentage

        FROM order_delivery_status d
        JOIN public.order_reviews r
            ON d.order_id = r.order_id

        WHERE r.review_score IS NOT NULL

        GROUP BY d.delivery_status
        ORDER BY d.delivery_status;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        return [
            {
                "delivery_status": row[0],
                "total_reviews": row[1],
                "average_review_score": float(row[2]),
                "low_rated_reviews": row[3],
                "low_rating_percentage": float(row[4])
            }
            for row in results
        ]

    finally:
        connection.close()
