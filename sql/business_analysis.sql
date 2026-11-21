-- 1. Total Orders and Unique Customers

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;


-- 2. Order Status Analysis
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- 3. Total Revenue Analysis
SELECT
    ROUND(SUM(payment_value)::numeric, 2) AS total_revenue
FROM order_payments;


-- 4. Monthly Revenue Analysis

SELECT
    DATE_TRUNC(
        'month',
        o.order_purchase_timestamp::timestamp
    ) AS month,
    ROUND(SUM(p.payment_value)::numeric, 2) AS revenue
FROM orders o
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY 1
ORDER BY 1;


-- 5. Top 10 Best-Selling Products

SELECT
    product_id,
    COUNT(*) AS total_sold
FROM order_items
GROUP BY product_id
ORDER BY total_sold DESC
LIMIT 10;


-- 6. Top 10 Product Categories

SELECT
    p.product_category_name,
    COUNT(oi.order_item_id) AS total_items_sold,
    ROUND(SUM(oi.price)::numeric, 2) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;



-- 7. Customer State Analysis

SELECT
    customer_state,
    COUNT(DISTINCT customer_id) AS total_customers
FROM customers
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;



-- 8. Seller Performance Analysis

SELECT
    seller_id,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(price)::numeric, 2) AS total_sales
FROM order_items
GROUP BY seller_id
ORDER BY total_sales DESC
LIMIT 10;



-- 9. Average Delivery Time Analysis

SELECT
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date::timestamp -
                    order_purchase_timestamp::timestamp
                )
            ) / 86400
        )::numeric, 2
    ) AS avg_delivery_days
FROM orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_purchase_timestamp IS NOT NULL;



-- 10. Late Delivery Analysis

SELECT
    COUNT(*) AS total_delivered_orders,
    COUNT(*) FILTER (
        WHERE order_delivered_customer_date::timestamp >
              order_estimated_delivery_date::timestamp
    ) AS late_delivered_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_delivered_customer_date::timestamp >
                  order_estimated_delivery_date::timestamp
        ) / COUNT(*), 2
    ) AS late_delivery_percentage
FROM orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL;



-- 11. Customer Review Analysis

SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM order_reviews
GROUP BY review_score
ORDER BY review_score DESC;

-- 1. TOTAL REVENUE ANALYSIS

SELECT
    ROUND(SUM(payment_value)::numeric, 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(payment_value)::numeric, 2) AS average_order_value
FROM public.order_payments;

-- 1. TOTAL ORDERS AND UNIQUE CUSTOMERS
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM public.orders;


-- 2. ORDER STATUS ANALYSIS
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM public.orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- 3. TOTAL REVENUE ANALYSIS
SELECT
    ROUND(SUM(payment_value)::numeric, 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS paid_orders,
    ROUND(AVG(payment_value)::numeric, 2) AS avg_payment_per_record
FROM public.order_payments;


-- 4. MONTHLY REVENUE ANALYSIS
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp::timestamp) AS month,
    ROUND(SUM(p.payment_value)::numeric, 2) AS revenue
FROM public.orders o
JOIN public.order_payments p
    ON o.order_id = p.order_id
GROUP BY 1
ORDER BY 1;


-- 5. TOP 10 BEST-SELLING PRODUCTS
SELECT
    product_id,
    COUNT(*) AS total_sold
FROM public.order_items
GROUP BY product_id
ORDER BY total_sold DESC
LIMIT 10;


-- 6. TOP 10 PRODUCT CATEGORIES
SELECT
    p.product_category_name,
    COUNT(oi.order_item_id) AS total_items_sold,
    ROUND(SUM(oi.price)::numeric, 2) AS total_revenue
FROM public.order_items oi
JOIN public.products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 7. CUSTOMER STATE ANALYSIS
SELECT
    customer_state,
    COUNT(DISTINCT customer_id) AS total_customers
FROM public.customers
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;


-- 8. SELLER PERFORMANCE ANALYSIS
SELECT
    seller_id,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(price)::numeric, 2) AS total_sales
FROM public.order_items
GROUP BY seller_id
ORDER BY total_sales DESC
LIMIT 10;


-- 9. AVERAGE DELIVERY TIME ANALYSIS
SELECT
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date::timestamp -
                    order_purchase_timestamp::timestamp
                )
            ) / 86400
        )::numeric, 2
    ) AS avg_delivery_days
FROM public.orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_purchase_timestamp IS NOT NULL;


-- 10. LATE DELIVERY ANALYSIS
SELECT
    COUNT(*) AS total_delivered_orders,
    COUNT(*) FILTER (
        WHERE order_delivered_customer_date::timestamp >
              order_estimated_delivery_date::timestamp
    ) AS late_delivered_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE order_delivered_customer_date::timestamp >
                  order_estimated_delivery_date::timestamp
        ) / COUNT(*), 2
    ) AS late_delivery_percentage
FROM public.orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
AND order_estimated_delivery_date IS NOT NULL;


-- 11. CUSTOMER REVIEW ANALYSIS
SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM public.order_reviews
GROUP BY review_score
ORDER BY review_score DESC;
