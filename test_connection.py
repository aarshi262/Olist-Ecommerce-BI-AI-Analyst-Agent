
import psycopg2
import pandas as pd
from getpass import getpass

DB_USER = input("PostgreSQL username [postgres]: ").strip() or "postgres"
DB_PASSWORD = getpass("PostgreSQL password: ")

try:
    connection = psycopg2.connect(
        database="business",
        user=DB_USER,
        password=DB_PASSWORD,
        host="localhost",
        port="5432"
    )

    query = """
SELECT
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_delivered_customer_date::timestamp >
                  order_estimated_delivery_date::timestamp
        ) / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM public.orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL;
"""

    df = pd.read_sql_query(query, connection)

    print("\nCustomer Analysis:")
    print(df)

    connection.close()

except Exception as error:
    print("Error:", error)
