from pathlib import Path

import pandas as pd

# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the raw dataset path
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"

# Load the Excel dataset
df = pd.read_excel(DATA_PATH)

# Display basic information
print("Dataset loaded successfully!")
print("-" * 50)

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst five rows:")
print(df.head())
# --------------------------------------------------
# DATA QUALITY CHECKS
# --------------------------------------------------

print("\n" + "=" * 50)
print("DATA QUALITY CHECKS")
print("=" * 50)

# 1. Inspect column data types
print("\n1. COLUMN DATA TYPES")
print(df.dtypes)

# 2. Count missing values
print("\n2. MISSING VALUES")
print(df.isnull().sum())

# 3. Count duplicate rows
print("\n3. DUPLICATE ROWS")
print("Duplicate rows:", df.duplicated().sum())

# 4. Inspect negative quantities
print("\n4. NEGATIVE QUANTITIES")
print("Rows with negative quantities:", (df["Quantity"] < 0).sum())

# 5. Inspect non-positive unit prices
print("\n5. NON-POSITIVE UNIT PRICES")
print("Rows with zero or negative prices:", (df["UnitPrice"] <= 0).sum())

# 6. Inspect cancellation invoices
print("\n6. CANCELLATION INVOICES")
print(
    "Invoice numbers starting with C:",
    df["InvoiceNo"].astype(str).str.startswith("C").sum()
)
# --------------------------------------------------
# FURTHER DATA INVESTIGATION
# --------------------------------------------------

print("\n" + "=" * 50)
print("FURTHER DATA INVESTIGATION")
print("=" * 50)

# 1. Percentage of missing customer IDs
missing_customer_count = df["CustomerID"].isna().sum()

missing_customer_percentage = (
    missing_customer_count / len(df)
) * 100

print("\n1. MISSING CUSTOMER ID ANALYSIS")
print("Missing customer IDs:", missing_customer_count)
print(f"Percentage missing: {missing_customer_percentage:.2f}%")

# 2. Negative quantities in cancellation invoices
cancellation_mask = (
    df["InvoiceNo"].astype(str).str.startswith("C")
)

negative_quantity_mask = df["Quantity"] < 0

print("\n2. CANCELLATION AND NEGATIVE QUANTITY ANALYSIS")
print(
    "Cancellation invoice rows:",
    cancellation_mask.sum()
)

print(
    "Negative quantity rows:",
    negative_quantity_mask.sum()
)

print(
    "Rows with both cancellation invoice and negative quantity:",
    (cancellation_mask & negative_quantity_mask).sum()
)

# 3. Inspect zero-price transactions
zero_price_rows = df[df["UnitPrice"] == 0]

print("\n3. ZERO-PRICE TRANSACTIONS")
print("Number of zero-price rows:", len(zero_price_rows))

print(
    zero_price_rows[
        ["InvoiceNo", "StockCode", "Description",
         "Quantity", "UnitPrice", "CustomerID"]
    ].head(10).to_string(index=False)
)

# 4. Basic business counts
print("\n4. BUSINESS COUNTS")
print("Unique invoices:", df["InvoiceNo"].nunique())
print("Unique products:", df["StockCode"].nunique())
print("Unique countries:", df["Country"].nunique())
print("Unique identified customers:", df["CustomerID"].nunique())
# --------------------------------------------------
# INVESTIGATE NEGATIVE QUANTITIES WITHOUT C INVOICE
# --------------------------------------------------

print("\n" + "=" * 50)
print("NEGATIVE QUANTITIES WITHOUT C INVOICE")
print("=" * 50)

# Identify negative quantities
negative_quantity_mask = df["Quantity"] < 0

# Identify invoices that do not start with C
non_cancellation_mask = (
    ~df["InvoiceNo"].astype(str).str.startswith("C")
)

# Select records meeting both conditions
negative_non_cancellation = df[
    negative_quantity_mask & non_cancellation_mask
]

print(
    "Number of records:",
    len(negative_non_cancellation)
)

print("\nFirst 20 records:")

print(
    negative_non_cancellation[
        [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "CustomerID",
            "Country",
        ]
    ].head(20).to_string(index=False)
)
# --------------------------------------------------
# INVESTIGATE NEGATIVE QUANTITIES WITHOUT C INVOICE
# --------------------------------------------------

print("\n" + "=" * 50)
print("NEGATIVE QUANTITIES WITHOUT C INVOICE")
print("=" * 50)

# Find rows with negative quantities
negative_quantity_mask = df["Quantity"] < 0

# Find invoice numbers that do not start with C
non_cancellation_mask = (
    ~df["InvoiceNo"].astype(str).str.startswith("C")
)

# Select rows satisfying both conditions
negative_non_cancellation = df[
    negative_quantity_mask & non_cancellation_mask
]

print("Number of records:", len(negative_non_cancellation))

print("\nFirst 20 records:")

print(
    negative_non_cancellation[
        [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "CustomerID",
            "Country",
        ]
    ].head(20).to_string(index=False)
)