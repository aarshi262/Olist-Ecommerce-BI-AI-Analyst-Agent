import pandas as pd
from pathlib import Path

data_folder = Path(__file__).resolve().parent

orders = pd.read_csv(data_folder / "olist_orders_dataset.csv")
customers = pd.read_csv(data_folder / "olist_customers_dataset.csv")
order_items = pd.read_csv(data_folder / "olist_order_items_dataset.csv")
payments = pd.read_csv(data_folder / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(data_folder / "olist_order_reviews_dataset.csv")
products = pd.read_csv(data_folder / "olist_products_dataset.csv")
sellers = pd.read_csv(data_folder / "olist_sellers_dataset.csv")
geolocation = pd.read_csv(data_folder / "olist_geolocation_dataset.csv")
category_translation = pd.read_csv(data_folder / "product_category_name_translation.csv")

print("Olist CSV files loaded successfully!")

print("\nDataset Overview:")
print("Orders:", orders.shape)
print("Customers:", customers.shape)
print("Order Items:", order_items.shape)
print("Payments:", payments.shape)
print("Reviews:", reviews.shape)
print("Products:", products.shape)
print("Sellers:", sellers.shape)
print("Geolocation:", geolocation.shape)
print("Category Translation:", category_translation.shape)

print("\n--- DATA QUALITY CHECK ---")

print("Orders missing values:")
print(orders.isnull().sum())

print("\nCustomers missing values:")
print(customers.isnull().sum())

print("\nDuplicate Order IDs:")
print(orders["order_id"].duplicated().sum())

print("\n--- ORDER STATUS ANALYSIS ---")

print(orders["order_status"].value_counts())
print("\n--- MISSING DELIVERY DATE BY STATUS ---")

print(
    orders.groupby("order_status")[
        "order_delivered_customer_date"
    ].apply(lambda x: x.isnull().sum())
)

print("\n--- DELIVERED ORDERS WITH MISSING DATES ---")

missing_delivered = orders[
    (orders["order_status"] == "delivered") &
    (orders["order_delivered_customer_date"].isnull())
]

print(missing_delivered)
print("\nTotal:", len(missing_delivered))
print("\n--- CHECKING 8 DELIVERED ORDERS ---")

print(
    missing_delivered[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    ].to_string(index=False)
)
print("\n--- MISSING VALUES PERCENTAGE ---")

missing_percentage = (
    orders.isnull().sum() / len(orders) * 100
).round(2)

print(missing_percentage)

print("\n--- DUPLICATE ROWS CHECK ---")

datasets = {
    "Orders": orders,
    "Customers": customers,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Products": products,
    "Sellers": sellers,
    "Geolocation": geolocation,
    "Category Translation": category_translation
}

for name, df in datasets.items():
    print(name, ":", df.duplicated().sum())
    print("\n--- GEOLOCATION DUPLICATE ANALYSIS ---")

print("Total Rows:", len(geolocation))

print(
    "Duplicate ZIP Code Prefix:",
    geolocation["geolocation_zip_code_prefix"].duplicated().sum()
)

print(
    "Unique ZIP Code Prefix:",
    geolocation["geolocation_zip_code_prefix"].nunique()
)

print(
    "Exact Duplicate Rows:",
    geolocation.duplicated().sum()
)
print("\n--- ZIP CODE COORDINATE ANALYSIS ---")

zip_coordinate_count = (
    geolocation.drop_duplicates(
        subset=[
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng"
        ]
    )
    .groupby("geolocation_zip_code_prefix")
    .size()
)
print("ZIP codes with multiple coordinates:",
      (zip_coordinate_count > 1).sum())

print("Maximum coordinates for one ZIP code:",
      zip_coordinate_count.max())
print("\n--- OVERALL DATA QUALITY SUMMARY ---")

datasets = {
    "Orders": orders,
    "Customers": customers,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Products": products,
    "Sellers": sellers,
    "Geolocation": geolocation,
    "Category Translation": category_translation
}

summary = []

for name, df in datasets.items():
    total_missing = df.isnull().sum().sum()

    summary.append({
        "Dataset": name,
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": total_missing,
        "Missing %": round(
            (total_missing / (df.shape[0] * df.shape[1])) * 100, 2
        ),
        "Duplicate Rows": df.duplicated().sum()
    })

summary_df = pd.DataFrame(summary)

print(summary_df.to_string(index=False))
print("\n--- REVIEWS MISSING VALUES ANALYSIS ---")
print(reviews.isnull().sum())

print("\n--- PRODUCTS MISSING VALUES ANALYSIS ---")
print(products.isnull().sum())

print("\n--- REVIEWS MISSING PERCENTAGE ---")
print((reviews.isnull().mean() * 100).round(2))

print("\n--- PRODUCTS MISSING PERCENTAGE ---")
print((products.isnull().mean() * 100).round(2))

print("\n--- PRODUCTS WITH MISSING CATEGORY ---")

missing_products = products[
    products["product_category_name"].isnull()
]

print(missing_products.head(10).to_string(index=False))

print("\nTotal Products:", len(missing_products))

print("\n--- PRODUCTS WITH MISSING DIMENSIONS ---")

missing_dimensions = products[
    products["product_weight_g"].isnull()
]

print(missing_dimensions.to_string(index=False))

print("\nTotal Products:", len(missing_dimensions))

print("\n--- PRODUCT ID DUPLICATE CHECK ---")

print(
    "Duplicate Product IDs:",
    products["product_id"].duplicated().sum()
)

print(
    "Unique Product IDs:",
    products["product_id"].nunique()
)

print("\n--- PAYMENTS DATA QUALITY CHECK ---")

print("Missing Values:")
print(payments.isnull().sum())

print("\nDuplicate Payment IDs:")
print(payments["order_id"].duplicated().sum())

print("\nPayment Types:")
print(payments["payment_type"].value_counts())

print("\n--- PAYMENT RECORD DUPLICATE CHECK ---")

print(
    "Duplicate Order + Payment Sequence:",
    payments.duplicated(
        subset=["order_id", "payment_sequential"]
    ).sum()
)

print(
    "Unique Payment Sequences:",
    payments["payment_sequential"].nunique()
)

print("\n--- PAYMENT VALUE VALIDATION ---")

print("Minimum Payment Value:", payments["payment_value"].min())
print("Maximum Payment Value:", payments["payment_value"].max())

print("Zero Payment Values:", (payments["payment_value"] == 0).sum())

print("Negative Payment Values:", (payments["payment_value"] < 0).sum())

print("\n--- ZERO PAYMENT RECORDS ---")

zero_payments = payments[payments["payment_value"] == 0]

print(zero_payments)
print("\nTotal Zero Payment Records:", len(zero_payments))
print("\n--- ZERO PAYMENT ORDER STATUS ---")

zero_order_ids = zero_payments["order_id"].unique()

zero_payment_orders = orders[
    orders["order_id"].isin(zero_order_ids)
]

print(
    zero_payment_orders[
        ["order_id", "order_status", "order_purchase_timestamp"]
    ].to_string(index=False)
)
print("\n--- PAYMENTS FINAL DATA QUALITY SUMMARY ---")

print("Total Payment Records:", len(payments))
print("Missing Values:", payments.isnull().sum().sum())
print("Duplicate Order + Sequence:",
      payments.duplicated(
          subset=["order_id", "payment_sequential"]
      ).sum())
print("Zero Payment Values:",
      (payments["payment_value"] == 0).sum())
print("Negative Payment Values:",
      (payments["payment_value"] < 0).sum())
print("Unique Orders:", payments["order_id"].nunique())
print("\n--- REVIEWS DATA QUALITY CHECK ---")

print("Missing Values:")
print(reviews.isnull().sum())

print("\nDuplicate Review IDs:")
print(reviews["review_id"].duplicated().sum())

print("\nReview Scores:")
print(reviews["review_score"].value_counts().sort_index())

print("\n--- DUPLICATE REVIEW ID INVESTIGATION ---")

duplicate_reviews = reviews[
    reviews["review_id"].duplicated(keep=False)
]

print("Total Duplicate Rows:", len(duplicate_reviews))

print(
    duplicate_reviews.sort_values("review_id").head(20).to_string(index=False)
)
print("\n--- REVIEW DUPLICATE ANALYSIS ---")

print(
    "Exact Duplicate Rows:",
    reviews.duplicated().sum()
)

print(
    "Unique Review IDs:",
    reviews["review_id"].nunique()
)

print(
    "Review IDs with Multiple Orders:",
    (reviews.groupby("review_id")["order_id"].nunique() > 1).sum()
)

print(
    "Maximum Orders per Review ID:",
    reviews.groupby("review_id")["order_id"].nunique().max()
)
print("\n--- REVIEW ID ORDER COUNT ---")

print(
    reviews.groupby("review_id")["order_id"]
    .nunique()
    .value_counts()
    .sort_index()
)
print("\n--- REVIEWS FINAL DATA QUALITY SUMMARY ---")

print("Total Review Records:", len(reviews))

print("Missing Values:", reviews.isnull().sum().sum())

print("Exact Duplicate Rows:", reviews.duplicated().sum())

print("Unique Review IDs:", reviews["review_id"].nunique())

print("Invalid Review Scores:",
      (~reviews["review_score"].between(1, 5)).sum())

print("Unique Orders:", reviews["order_id"].nunique())

print("\n--- SELLERS DATA QUALITY CHECK ---")

print("Missing Values:")
print(sellers.isnull().sum())

print("\nDuplicate Seller IDs:")
print(sellers["seller_id"].duplicated().sum())

print("\nUnique Seller IDs:")
print(sellers["seller_id"].nunique())

print("\n--- SELLER STATE DISTRIBUTION ---")

print(sellers["seller_state"].value_counts())

print("\nTotal Seller States:",
      sellers["seller_state"].nunique())
print("\n--- SELLER ID VALIDATION ---")

print("Blank Seller IDs:",
      (sellers["seller_id"].str.strip() == "").sum())

print("Seller ID Data Type:",
      sellers["seller_id"].dtype)

print("Seller ID Length:")
print(sellers["seller_id"].str.len().value_counts())

print("\n--- SELLERS FINAL DATA QUALITY SUMMARY ---")

print("Total Seller Records:", len(sellers))

print("Missing Values:", sellers.isnull().sum().sum())

print("Duplicate Seller IDs:",
      sellers["seller_id"].duplicated().sum())

print("Unique Seller IDs:", sellers["seller_id"].nunique())

print("Unique Seller States:", sellers["seller_state"].nunique())

print("Blank Seller IDs:",
      (sellers["seller_id"].str.strip() == "").sum())

print("\n--- CUSTOMERS DATA QUALITY CHECK ---")

print("Missing Values:")
print(customers.isnull().sum())

print("\nDuplicate Customer IDs:")
print(customers["customer_id"].duplicated().sum())

print("\nUnique Customer IDs:")
print(customers["customer_id"].nunique())

print("\n--- CUSTOMER UNIQUE ID ANALYSIS ---")

print("Unique Customer IDs:",
      customers["customer_id"].nunique())

print("Unique Customer Unique IDs:",
      customers["customer_unique_id"].nunique())

print("Repeated Customer Unique IDs:",
      customers["customer_unique_id"].duplicated().sum())

print("\n--- CUSTOMER STATE DISTRIBUTION ---")

print(customers["customer_state"].value_counts())

print("\nTotal Customer States:",
      customers["customer_state"].nunique())
print("\n--- CUSTOMER ID VALIDATION ---")

print("Blank Customer IDs:",
      (customers["customer_id"].str.strip() == "").sum())

print("Customer ID Length:")
print(customers["customer_id"].str.len().value_counts())

print("\nCustomer Unique ID Length:")
print(customers["customer_unique_id"].str.len().value_counts())

print("\n--- CUSTOMERS FINAL DATA QUALITY SUMMARY ---")

print("Total Customer Records:", len(customers))

print("Missing Values:", customers.isnull().sum().sum())

print("Duplicate Customer IDs:",
      customers["customer_id"].duplicated().sum())

print("Unique Customer IDs:",
      customers["customer_id"].nunique())

print("Unique Customer Unique IDs:",
      customers["customer_unique_id"].nunique())

print("Unique Customer States:",
      customers["customer_state"].nunique())

print("\n--- PRODUCTS DATA QUALITY CHECK ---")

print("Missing Values:")
print(products.isnull().sum())

print("\nDuplicate Product IDs:")
print(products["product_id"].duplicated().sum())

print("\nUnique Product IDs:")
print(products["product_id"].nunique())

print("\n--- MISSING PRODUCT CATEGORY INVESTIGATION ---")

missing_category = products[
    products["product_category_name"].isnull()
]

print("Products with Missing Category:", len(missing_category))

print("\nMissing Values in These Products:")
print(missing_category.isnull().sum())

print("\nFirst 10 Records:")
print(missing_category.head(10).to_string(index=False))

print("\n--- MISSING PRODUCT DIMENSIONS INVESTIGATION ---")

missing_dimensions = products[
    products[
        [
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    ].isnull().any(axis=1)
]

print("Products with Missing Dimensions:", len(missing_dimensions))

print(missing_dimensions.to_string(index=False))

print("\n--- PRODUCT ID VALIDATION ---")

print("Blank Product IDs:",
      (products["product_id"].str.strip() == "").sum())

print("Product ID Length:")
print(products["product_id"].str.len().value_counts())
print("\n--- PRODUCTS FINAL DATA QUALITY SUMMARY ---")

print("Total Product Records:", len(products))

print("Missing Values:", products.isnull().sum().sum())

print("Duplicate Product IDs:",
      products["product_id"].duplicated().sum())

print("Unique Product IDs:", products["product_id"].nunique())

print("Missing Product Categories:",
      products["product_category_name"].isnull().sum())

print("Products with Missing Dimensions:",
      products[
          [
              "product_weight_g",
              "product_length_cm",
              "product_height_cm",
              "product_width_cm"
          ]
      ].isnull().any(axis=1).sum())
print("\n--- ORDER ITEMS DATA QUALITY CHECK ---")

print("Missing Values:")
print(order_items.isnull().sum())

print("\nDuplicate Rows:")
print(order_items.duplicated().sum())

print("\nTotal Order Items:", len(order_items))
print("\n--- ORDER ITEM ID DUPLICATE CHECK ---")

print(
    "Duplicate Order + Item ID:",
    order_items.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)

print(
    "Unique Order IDs:",
    order_items["order_id"].nunique()
)

print(
    "Unique Product IDs:",
    order_items["product_id"].nunique()
)
print("\n--- ORDER ITEMS PRICE VALIDATION ---")

print("Price Minimum:", order_items["price"].min())
print("Price Maximum:", order_items["price"].max())

print("Zero Price Records:", (order_items["price"] == 0).sum())
print("Negative Price Records:", (order_items["price"] < 0).sum())

print("Freight Minimum:", order_items["freight_value"].min())
print("Freight Maximum:", order_items["freight_value"].max())

print("Zero Freight Records:", (order_items["freight_value"] == 0).sum())
print("Negative Freight Records:", (order_items["freight_value"] < 0).sum())

print("\n--- ZERO FREIGHT INVESTIGATION ---")

zero_freight = order_items[
    order_items["freight_value"] == 0
]

print("Zero Freight Records:", len(zero_freight))

print("\nPrice Summary:")
print(zero_freight["price"].describe())

print("\nSample Zero Freight Records:")
print(
    zero_freight[
        ["order_id", "order_item_id", "product_id",
         "seller_id", "price", "freight_value"]
    ].head(10)
)
print("\n--- ORDER ITEMS FINAL DATA QUALITY SUMMARY ---")

print("Total Order Items:", len(order_items))

print("Missing Values:", order_items.isnull().sum().sum())

print("Exact Duplicate Rows:", order_items.duplicated().sum())

print(
    "Duplicate Order + Item ID:",
    order_items.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)

print("Unique Orders:", order_items["order_id"].nunique())

print("Unique Products:", order_items["product_id"].nunique())

print("Zero Freight Records:", (order_items["freight_value"] == 0).sum())

print("Negative Price Records:", (order_items["price"] < 0).sum())

print("Negative Freight Records:", (order_items["freight_value"] < 0).sum())

print("\n--- GEOLOCATION DATA QUALITY CHECK ---")

print("Total Geolocation Records:", len(geolocation))

print("\nMissing Values:")
print(geolocation.isnull().sum())

print("\nExact Duplicate Rows:")
print(geolocation.duplicated().sum())

print("\nUnique ZIP Code Prefixes:")
print(geolocation["geolocation_zip_code_prefix"].nunique())

print("\nLatitude Range:")
print(
    geolocation["geolocation_lat"].min(),
    "to",
    geolocation["geolocation_lat"].max()
)

print("\nLongitude Range:")
print(
    geolocation["geolocation_lng"].min(),
    "to",
    geolocation["geolocation_lng"].max()
)
print("\n--- GEOLOCATION COORDINATE VALIDATION ---")

invalid_coordinates = geolocation[
    (geolocation["geolocation_lat"] < -34) |
    (geolocation["geolocation_lat"] > 6) |
    (geolocation["geolocation_lng"] < -75) |
    (geolocation["geolocation_lng"] > -30)
]

print("Out-of-range Coordinate Records:", len(invalid_coordinates))

print("\nSample Out-of-range Records:")
print(invalid_coordinates.head(10))
print("\n--- GEOLOCATION STATE ANALYSIS ---")

print("Unique States:", geolocation["geolocation_state"].nunique())

print("\nRecords by State:")
print(
    geolocation["geolocation_state"]
    .value_counts()
)

print("\nUnique Cities:", geolocation["geolocation_city"].nunique())
print("\n--- CATEGORY TRANSLATION DATA QUALITY CHECK ---")

print("Total Records:", len(category_translation))

print("\nMissing Values:")
print(category_translation.isnull().sum())

print("\nExact Duplicate Rows:")
print(category_translation.duplicated().sum())

print("\nDuplicate Category Names:")
print(
    category_translation["product_category_name"]
    .duplicated().sum()
)

print("\nUnique Portuguese Categories:")
print(category_translation["product_category_name"].nunique())

print("\nUnique English Categories:")
print(category_translation["product_category_name_english"].nunique())

print("\n--- FINAL CONSOLIDATED DATA QUALITY REPORT ---")

datasets = {
    "Orders": orders,
    "Customers": customers,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Products": products,
    "Sellers": sellers,
    "Geolocation": geolocation,
    "Category Translation": category_translation
}

report = []

for name, df in datasets.items():
    report.append({
        "Dataset": name,
        "Total Rows": len(df),
        "Total Columns": len(df.columns),
        "Missing Values": df.isnull().sum().sum(),
        "Missing %": round(
            (df.isnull().sum().sum() /
             (len(df) * len(df.columns))) * 100, 2
        ),
        "Exact Duplicate Rows": df.duplicated().sum()
    })

quality_report = pd.DataFrame(report)

print(quality_report.to_string(index=False))

quality_report.to_csv(
    "data_quality_report.csv",
    index=False
)

print("\nData Quality Report saved successfully!")