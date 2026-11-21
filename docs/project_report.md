 ##  Olist E-Commerce Business Intelligence & AI Analyst Agent ## 

# Project Overview

   - The Olist E-Commerce Business Intelligence & AI Analyst Agent is an end-to-end data analytics project that evaluates e-commerce business performance using SQL, Python, PostgreSQL, and Power BI.

   - The project examines key business areas, including sales revenue, customer behavior, product category performance, payment methods, customer reviews, and delivery performance, to support data-driven decision-making.

# Project Objectives
  - Analyze the overall performance of the e-commerce business.
  - Identify top-performing product categories.
  - Understand the geographic distribution of customers across states.
  - Evaluate payment methods and their contribution to revenue.
  - Assess customer satisfaction through review scores and feedback.
  - Monitor on-time and late delivery performance.
  - Generate actionable business insights through data analysis.

# Tools and Technologies
                   Category	                            Tools
             Programming & Analysis	              Python, Pandas, Matplotlib
              Database & Querying	                 PostgreSQL, SQL
              Data Visualization	                    Power BI
             Development Environment	                VS Code

# Dataset Overview

   The project uses nine Olist dataset CSV files:

  - Orders: order status, purchase and delivery timestamps
  - Customers: customer identifiers and location details
  - Order Items: products, sellers, prices, and freight values per order
  - Order Payments: payment types, installments, and payment values
  - Order Reviews: customer review scores and comments
  - Products: product attributes and category information
  - Sellers: seller identifiers and location details
  - Geolocation: zip code-level latitude and longitude data
  - Product Category Translation: Portuguese-to-English category name mapping

# Data Cleaning and Quality Checks

  -  Data quality checks were performed using Python and Pandas to identify missing values, duplicate records, and inconsistencies across the nine datasets.

 ## Checks Performed

   1.  Checked for missing values across all datasets.
   2.  Identified duplicate records in each dataset.
   3.  Verified the uniqueness of customer, order, product, and seller identifiers.
   4.  Examined repeated records in the geolocation dataset.
   5.  Investigated missing delivery timestamps in the orders dataset.
   6.  Validated payment records and duplicate payment sequences.
   7.  Reviewed customer review scores and product information.

 ## Key Findings

            Dataset	                           Number of Records
            Orders	                                99,441
           Customers	                            99,441
           Order Items	                            112,650
           Order Payments	                        103,886
           Order Reviews                        	99,224
             Products	                            32,951
             Sellers	                            3,095
           Geolocation	                           1,000,163
       Product Category Translation	                 71

 ## Data Handling Approach

   - Missing and repeated values were investigated carefully before any action was taken. Records were not automatically deleted or modified when they represented valid business scenarios, such as undelivered or canceled orders without delivery timestamps, or repeated geolocation entries for the same zip code prefix.

# SQL Business Analysis

   - SQL was used with PostgreSQL to perform business analysis and extract meaningful insights from the Olist e-commerce dataset.

 ## SQL Analyses Performed

1. Total Orders and Unique Customers
2. Order Status Analysis
3. Total Revenue Analysis
4. Monthly Revenue Trend
5. Top 10 Best-Selling Products
6. Top 10 Product Categories by Revenue
7. Customer State Analysis
8. Seller Performance Analysis
9. Average Delivery Time Analysis
10. Late Delivery Analysis
11. Customer Review Analysis

 ## Key Business Findings

- Total Orders: 99,441
- Unique Customers: 99,441
- Total Revenue: ₹16,008,872.12
- Average Delivery Time: 12.56 days
- Late Delivery Rate: 8.11%
- Highest Monthly Revenue: November 2017 (₹11,94,882.80)
- Top Revenue Category: Health & Beauty
- Highest Customer State: São Paulo (SP)
- Most Used Payment Method: Credit Card
- Highest Customer Review Score: 5 Stars

# Python Business Analysis

- Python and Pandas were used to perform business analysis by retrieving data from PostgreSQL through SQLAlchemy.

 ## Analysis Performed

- Revenue analysis
- Customer analysis
- Order status analysis
- Monthly revenue analysis
- Top-selling product analysis
- Product category revenue analysis
- Customer state analysis
- Seller performance analysis
- Average delivery time analysis
- Late delivery analysis
- Customer review analysis

 ## Data Visualization

Matplotlib was used to create the following visualizations:

1. Monthly Revenue Trend
2. Top 10 Product Categories by Revenue
3. Customer State Analysis
4. Payment Type Revenue Distribution
5. Customer Review Score Distribution
6. Late vs On-Time Delivery Analysis

# Power BI Dashboard

- Power BI was used to create an interactive business intelligence dashboard to present key business metrics and performance indicators.

 ## Key Performance Indicators (KPIs)

- Total Orders: 99,441
- Unique Customers: 99,441
- Total Revenue: ₹16.01 Million
- Average Delivery Days: 12.50
- Late Delivery Percentage: 8.11%

Note: The Power BI dashboard reports average delivery time as 12.50 days using calendar-date differences, while the SQL and Python analysis reports 12.56 days using exact timestamp differences.

 ## Dashboard Visualizations

- Monthly Revenue Trend
- Top 10 Product Categories
- Customer State Analysis
- Payment Type Revenue Distribution
- Customer Review Score Distribution
- Order Status Distribution
- Late vs On-Time Delivery Analysis

The dashboard helps users understand business performance through interactive charts, KPIs, and visual insights.

# Key Business Insights

The analysis of the Olist e-commerce dataset revealed the following business insights:

1. Revenue Performance: The business generated approximately ₹16.01 million in total revenue.
2. Monthly Revenue: November 2017 recorded the highest monthly revenue.
3. Product Performance: Health & Beauty was the highest revenue-generating product category.
4. Customer Distribution: São Paulo (SP) had the highest number of customers.
5. Payment Behavior: Credit cards were the most commonly used payment method.
6. Customer Satisfaction: 5-star reviews represented the largest share of customer reviews.
7. Delivery Performance: 8.11% of delivered orders with available delivery dates were late.

These findings can help businesses understand sales performance, customer preferences, and delivery efficiency.

# Conclusion

1. The Olist E-Commerce Business Intelligence & AI Analyst Agent project demonstrates an end-to-end data analytics workflow using PostgreSQL, SQL, Python, Pandas, Matplotlib, and Power BI.

2. The project involved data loading, data quality assessment, SQL-based business analysis, Python analysis, and interactive dashboard development.

3. The findings provide useful insights into revenue trends, customer behavior, product performance, payment  preferences, customer satisfaction, and delivery efficiency.

4. This project strengthened practical skills in data analysis, database management, SQL querying, Python programming, and business intelligence reporting.
