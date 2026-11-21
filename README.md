# Olist E-Commerce Business Intelligence & AI Analyst Agent

An end-to-end e-commerce data analytics project focused on analyzing business performance, customer behavior, revenue trends, product categories, payment methods, customer reviews, and delivery efficiency.

## Project Overview

The project uses the Olist e-commerce dataset to transform raw business data into meaningful insights using SQL, Python, PostgreSQL, and Power BI.

The analytics workflow includes:
- Data loading and quality assessment
- SQL-based business analysis
- Python and Pandas data analysis
- Data visualization using Matplotlib
- Interactive Power BI dashboard development

## Project Objectives

- Analyze overall e-commerce business performance.
- Identify top-performing products and categories.
- Understand customer distribution across states.
- Evaluate payment methods and revenue contribution.
- Analyze customer satisfaction and review scores.
- Measure delivery performance and late deliveries.
- Generate actionable business insights.

## Tools & Technologies

                      Category                                           Technologies 

                    Programming                                            Python 
                    Data Analysis                                          Pandas 
                  Data Visualization                                   Matplotlib, Power BI 
                     Database                                             PostgreSQL 
                   Query Language                                           SQL 
                 Development Environment                                   VS Code 

## Dataset Overview

The project uses nine Olist CSV datasets:

1. Orders
2. Customers
3. Order Items
4. Order Payments
5. Order Reviews
6. Products
7. Sellers
8. Geolocation
9. Product Category Translation

## Key Performance Indicators

          KPI                     Result 

       Total Orders               99,441 
     Unique Customers             99,441  
      Total Revenue            ₹16.01 Million 
     Average Delivery Days        12.50 
      Late Delivery Rate          8.11% 

## Business Analysis

### SQL Analysis
- Total orders and unique customers
- Order status analysis
- Revenue analysis
- Monthly revenue trends
- Top 10 best-selling products
- Top 10 product categories by revenue
- Customer state analysis
- Seller performance
- Average delivery time
- Late delivery analysis
- Customer review analysis

### Python Analysis
- Revenue and customer analysis
- Monthly revenue analysis
- Product and category performance
- Customer state analysis
- Seller performance
- Delivery performance
- Customer review analysis

## Data Visualizations

Six visualizations were created using Matplotlib:

- Monthly Revenue Trend
- Top 10 Product Categories by Revenue
- Customer State Analysis
- Payment Type Revenue Distribution
- Customer Review Score Distribution
- Late vs On-Time Delivery Analysis

### Visualization Gallery

#### 1. Monthly Revenue Trend
 ![Monthly Revenue Trend](visualizations/monthly_revenue_trend.png)

#### 2. Top 10 Product Categories
 ![Top 10 Categories](visualizations/top_10_categories_revenue.png)

#### 3. Customer State Analysis
 ![Customer State Analysis](visualizations/customer_state_analysis.png)

#### 4. Payment Type Distribution
 ![Payment Type Distribution](visualizations/payment_type_distribution.png)

#### 5. Customer Review Analysis
 ![Customer Review Analysis](visualizations/customer_review_analysis.png)

#### 6. Delivery Performance
 ![Delivery Performance](visualizations/delivery_performance_analysis.png)


## Power BI Dashboard

An interactive Power BI dashboard was developed to monitor key business metrics and visualize e-commerce performance.

Dashboard includes:
- KPI Cards
- Monthly Revenue Trend
- Top 10 Product Categories
- Customer State Analysis
- Payment Type Revenue Distribution
- Customer Review Score Distribution
- Order Status Distribution
- Delivery Performance Analysis

  ### Dashboard Preview

  ![Olist Power BI Dashboard](visualizations/power_bi_dashboard.png)

## Key Business Insights

- Total revenue reached approximately ₹16.01 million.
- November 2017 recorded the highest monthly revenue.
- Health & Beauty was the highest revenue-generating category.
- São Paulo (SP) had the highest customer count.
- Credit cards were the most commonly used payment method.
- 5-star reviews represented the largest review group.
- 8.11% of delivered orders with available delivery dates were late.

## Project Structure

```text
AI-Businness-Intelligence-Agent/
│
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   └── product_category_name_translation.csv
│   └── load_olist_data.py
├── docs/
│   └── project_report.md
│
├── sql/
│   └── business_analysis.sql
│
├── python_business_analysis.py
├── python_visualizations.py
├── data_quality_report.csv
└── README.md
```

## Project Documentation

For detailed methodology, data quality checks, SQL findings, Python analysis, and dashboard details, see [Project Report](docs/project_report.md).

## Future Enhancements

- Integrate Claude AI for natural-language business questions.
- Build an AI-powered business analyst assistant.
- Automate analytical workflows using n8n.
- Deploy the application for live access.

## Conclusion

This project demonstrates practical experience in data analytics, SQL querying, Python programming, database management, data visualization, and business intelligence reporting.

**Project Status:** Core data analytics and Power BI dashboard completed. AI agent integration and deployment are planned future enhancements.