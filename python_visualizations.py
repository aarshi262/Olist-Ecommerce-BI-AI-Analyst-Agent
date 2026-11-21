import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, URL
import getpass

password = getpass.getpass("Enter PostgreSQL password: ")

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=password,
    host="localhost",
    port=5432,
    database="business"
)

engine = create_engine(connection_url)

print("Database Connected Successfully!")


query = """
SELECT
    TO_CHAR(o.order_purchase_timestamp::timestamp, 'YYYY-MM') AS month,
    SUM(p.payment_value) AS revenue
FROM public.orders o
JOIN public.order_payments p
    ON o.order_id = p.order_id
GROUP BY month
ORDER BY month;
"""

monthly_data = pd.read_sql_query(query, engine)

print("\nMonthly Revenue Data:")
print(monthly_data)
category_query = """
SELECT
    ct.product_category_name_english AS category,
    SUM(oi.price) AS revenue
FROM public.order_items oi
JOIN public.products p
    ON oi.product_id = p.product_id
JOIN public.category_translation ct
    ON p.product_category_name = ct.product_category_name
GROUP BY ct.product_category_name_english
ORDER BY revenue DESC
LIMIT 10;
"""

category_data = pd.read_sql_query(category_query, engine)

print("\nTop 10 Product Categories by Revenue:")
print(category_data)
plt.figure(figsize=(12, 6))

plt.barh(
    category_data["category"],
    category_data["revenue"]
)

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product Category")

plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("top_10_categories_revenue.png", dpi=300)
plt.show()

state_query = """
SELECT
    customer_state AS state,
    COUNT(customer_id) AS total_customers
FROM public.customers
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;
"""

state_data = pd.read_sql_query(state_query, engine)

print("\nTop 10 Customer States:")
print(state_data)

plt.figure(figsize=(10, 6))

plt.bar(
    state_data["state"],
    state_data["total_customers"]
)

plt.title("Top 10 Customer States by Customers")
plt.xlabel("State")
plt.ylabel("Total Customers")

plt.tight_layout()

plt.savefig("customer_state_analysis.png", dpi=300)
plt.show()

payment_query = """
SELECT
    payment_type,
    COUNT(*) AS total_transactions,
    SUM(payment_value) AS total_revenue
FROM public.order_payments
GROUP BY payment_type
ORDER BY total_revenue DESC;
"""

payment_data = pd.read_sql_query(payment_query, engine)

print("\nPayment Type Analysis:")
print(payment_data)

plt.figure(figsize=(9, 6))

def show_percentage(pct):
    return f"{pct:.1f}%" if pct >= 5 else ""

wedges, texts, autotexts = plt.pie(
    payment_data["total_revenue"],
    autopct=show_percentage,
    startangle=90
)

plt.legend(
    wedges,
    payment_data["payment_type"],
    title="Payment Type",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1)
)

plt.title("Revenue Distribution by Payment Type")
plt.tight_layout()

plt.savefig("payment_type_distribution.png", dpi=300)
plt.show()

review_query = """
SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM public.order_reviews
GROUP BY review_score
ORDER BY review_score;
"""

review_data = pd.read_sql_query(review_query, engine)

print("\nCustomer Review Analysis:")
print(review_data)

plt.figure(figsize=(9, 6))

plt.bar(
    review_data["review_score"],
    review_data["total_reviews"]
)

plt.title("Customer Review Score Distribution")
plt.xlabel("Review Score")
plt.ylabel("Total Reviews")

plt.xticks([1, 2, 3, 4, 5])
plt.tight_layout()

plt.savefig("customer_review_analysis.png", dpi=300)
plt.show()

delivery_query = """
SELECT
    CASE
        WHEN order_delivered_customer_date::timestamp >
             order_estimated_delivery_date::timestamp
        THEN 'Late Delivery'
        ELSE 'On-Time Delivery'
    END AS delivery_status,
    COUNT(*) AS total_orders
FROM public.orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL
GROUP BY delivery_status;
"""

delivery_data = pd.read_sql_query(delivery_query, engine)

print("\nDelivery Performance Analysis:")
print(delivery_data)

plt.figure(figsize=(9, 6))

plt.bar(
    delivery_data["delivery_status"],
    delivery_data["total_orders"]
)

plt.title("Late vs On-Time Delivery Analysis")
plt.xlabel("Delivery Status")
plt.ylabel("Total Orders")

plt.tight_layout()

plt.savefig("delivery_performance_analysis.png", dpi=300)
plt.show()

engine.dispose()

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_data["month"],
    monthly_data["revenue"],
    marker="o"
)

plt.title("Olist Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("monthly_revenue_trend.png", dpi=300)
plt.show()