
from ai_agent.database import get_database_columns

columns = get_database_columns()

for table, column in columns:
    print(f"{table} -> {column}")


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
                AVG(
                    EXTRACT(EPOCH FROM (
                        order_delivered_customer_date -
                        order_purchase_timestamp
                    )) / 86400
                )::numeric, 2
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
