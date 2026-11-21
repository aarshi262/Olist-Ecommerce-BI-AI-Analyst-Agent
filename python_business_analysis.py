import psycopg2
import pandas as pd
import getpass
from sqlalchemy import create_engine, URL
password = getpass.getpass("Enter PostgreSQL password: ")

try:
    conn = psycopg2.connect(
        host="localhost",
        database="business",
        user="postgres",
        password=password,
        port="5432"
    )

    print("PostgreSQL Database Connected Successfully!")
    engine = create_engine(
        URL.create(
            drivername="postgresql+psycopg2",
            username="postgres",
            password=password,
            host="localhost",
            port=5432,
            database="business"
        )
    )

    print("SQLAlchemy Engine Created Successfully!")

except Exception as e:
    print("Database Connection Failed:", e)
    

query = """
SELECT
    ROUND(SUM(payment_value)::numeric, 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_paid_orders,
    ROUND(AVG(payment_value)::numeric, 2) AS avg_payment_value
FROM public.order_payments;
"""

revenue_data = pd.read_sql_query(query, engine)

print("\n--- REVENUE ANALYSIS ---")
print(revenue_data)


query = """
SELECT
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT customer_state) AS total_states
FROM public.customers;
"""

customer_data = pd.read_sql_query(query, engine)

print("\n--- CUSTOMER ANALYSIS ---")
print(customer_data)


query = """
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM public.orders
GROUP BY order_status
ORDER BY total_orders DESC;
"""

status_data = pd.read_sql_query(query, engine)

print("\n--- ORDER STATUS ANALYSIS ---")
print(status_data)


query = """
SELECT
    TO_CHAR(o.order_purchase_timestamp::timestamp, 'YYYY-MM') AS month,
    ROUND(SUM(p.payment_value)::numeric, 2) AS monthly_revenue
FROM public.orders o
JOIN public.order_payments p
    ON o.order_id = p.order_id
GROUP BY month
ORDER BY month;
"""
monthly_data = pd.read_sql_query(query, engine)
print("\n--- MONTHLY REVENUE ANALYSIS ---")
print(monthly_data)

query = """
SELECT
    product_id,
    COUNT(*) AS units_sold
FROM public.order_items
GROUP BY product_id
ORDER BY units_sold DESC
LIMIT 10;
"""

top_products = pd.read_sql_query(query, engine)

print("\n--- TOP 10 BEST-SELLING PRODUCTS ---")
print(top_products)

query = """
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name) AS category,
    COUNT(*) AS items_sold,
    ROUND(SUM(oi.price)::numeric, 2) AS total_revenue
FROM public.order_items oi
JOIN public.products p
    ON oi.product_id = p.product_id
LEFT JOIN public.category_translation t
    ON p.product_category_name = t.product_category_name
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 10;
"""

category_data = pd.read_sql_query(query, engine)

print("\n--- TOP 10 PRODUCT CATEGORIES BY REVENUE ---")
print(category_data)

query = """
SELECT
    customer_state,
    COUNT(DISTINCT customer_id) AS total_customers
FROM public.customers
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;
"""

state_data = pd.read_sql_query(query, engine)

print("\n--- CUSTOMER STATE ANALYSIS ---")
print(state_data)

query = """
SELECT
    s.seller_id,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(oi.price)::numeric, 2) AS total_sales
FROM public.sellers s
JOIN public.order_items oi
    ON s.seller_id = oi.seller_id
GROUP BY s.seller_id
ORDER BY total_sales DESC
LIMIT 10;
"""

seller_data = pd.read_sql_query(query, engine)

print("\n--- SELLER PERFORMANCE ANALYSIS ---")
print(seller_data)

query = """
SELECT
    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                order_delivered_customer_date::timestamp
                - order_purchase_timestamp::timestamp
            )) / 86400
        )::numeric,
        2
    ) AS avg_delivery_days
FROM public.orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL;
"""

delivery_data = pd.read_sql_query(query, engine)

print("\n--- AVERAGE DELIVERY TIME ANALYSIS ---")
print(delivery_data)

query = """
SELECT
    COUNT(*) AS total_delivered_orders,
    COUNT(*) FILTER (
        WHERE order_delivered_customer_date::timestamp >
              order_estimated_delivery_date::timestamp
    ) AS late_orders,
    ROUND(
        COUNT(*) FILTER (
            WHERE order_delivered_customer_date::timestamp >
                  order_estimated_delivery_date::timestamp
        ) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM public.orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL;
"""
late_data = pd.read_sql_query(query, engine)

print("\n--- LATE DELIVERY ANALYSIS ---")
print(late_data)

query = """
SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM public.order_reviews
GROUP BY review_score
ORDER BY review_score DESC;
"""

review_data = pd.read_sql_query(query, engine)

print("\n--- CUSTOMER REVIEW ANALYSIS ---")
print(review_data)