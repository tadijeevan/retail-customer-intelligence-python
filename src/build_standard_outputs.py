from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"


def build_cleaned_transactions() -> None:
    """Create the standardized transaction output without deleting rows."""

    source = PROCESSED_DIR / "online_retail_prepared.csv"
    destination = PROCESSED_DIR / "cleaned_transactions.csv"

    df = pd.read_csv(
        source,
        dtype={
            "invoiceno": "string",
            "stockcode": "string",
            "description": "string",
            "country": "string",
        },
    )

    df["invoicedate"] = pd.to_datetime(
        df["invoicedate"], errors="coerce"
    )

    original_columns = {
        "invoiceno",
        "stockcode",
        "description",
        "quantity",
        "invoicedate",
        "unitprice",
        "customerid",
        "country",
        "is_cancellation",
        "line_value",
    }

    missing_columns = original_columns.difference(df.columns)

    if missing_columns:
        raise ValueError(
            f"Prepared transactions are missing columns: {sorted(missing_columns)}"
        )

    if df["invoicedate"].isna().any():
        raise ValueError(
            "Invalid invoice dates found in prepared transaction data."
        )

    if df["line_value"].isna().any():
        raise ValueError(
            "Missing line values found in prepared transaction data."
        )

    df.to_csv(destination, index=False, date_format="%Y-%m-%d %H:%M:%S")

    print("\nCLEANED TRANSACTIONS")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Output: {destination}")


def build_customer_features() -> None:
    """Combine existing customer-level reports into one feature dataset."""

    spending_path = REPORTS_DIR / "customer_spending_analysis.csv"
    rfm_path = REPORTS_DIR / "customer_rfm_scored.csv"
    frequency_path = REPORTS_DIR / "customer_purchase_frequency.csv"
    destination = PROCESSED_DIR / "customer_features.csv"

    spending = pd.read_csv(spending_path)
    rfm = pd.read_csv(rfm_path)
    frequency = pd.read_csv(frequency_path)

    # Normalize customer identifiers before merging.
    spending["customer_id"] = pd.to_numeric(
        spending["customer_id"], errors="coerce"
    )
    rfm["customer_id"] = pd.to_numeric(
        rfm["customer_id"], errors="coerce"
    )
    frequency["customerid"] = pd.to_numeric(
        frequency["customerid"], errors="coerce"
    )

    # RFM scores provide the recency, frequency, monetary and score features.
    rfm_columns = [
        "customer_id",
        "recency_days",
        "R_score",
        "F_score",
        "M_score",
        "RFM_score",
        "RFM_total_score",
    ]

    spending_columns = [
        "customer_id",
        "total_transaction_value",
        "positive_transaction_value",
        "total_units_net",
        "distinct_products",
    ]

    frequency_columns = [
        "customerid",
        "cancellation_invoice_count",
    ]

    features = rfm[rfm_columns].merge(
        spending[spending_columns],
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    features = features.merge(
        frequency[frequency_columns],
        left_on="customer_id",
        right_on="customerid",
        how="left",
        validate="one_to_one",
    )

    features = features.drop(columns=["customerid"])

    if features["customer_id"].isna().any():
        raise ValueError("Missing customer IDs found in customer features.")

    if features["customer_id"].duplicated().any():
        raise ValueError("Duplicate customers found in customer features.")

    if len(features) != len(rfm):
        raise ValueError(
            "Customer feature row count does not match the RFM scored dataset."
        )

    features.to_csv(destination, index=False)

    print("\nCUSTOMER FEATURES")
    print(f"Customers: {len(features):,}")
    print(f"Columns: {len(features.columns)}")
    print(f"Output: {destination}")
    print("\nFeature columns:")
    print(", ".join(features.columns))


def build_monthly_sales() -> None:
    """Create a standardized copy of the existing monthly sales report."""

    source = REPORTS_DIR / "monthly_sales_analysis.csv"
    destination = REPORTS_DIR / "monthly_sales.csv"

    df = pd.read_csv(source)

    required_columns = {
        "Month",
        "Sales_Value",
        "MoM_Growth_Percent",
    }

    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise ValueError(
            f"Monthly sales report is missing columns: {sorted(missing_columns)}"
        )

    df["Month"] = pd.to_datetime(
        df["Month"], format="%Y-%m", errors="raise"
    ).dt.to_period("M").astype(str)

    df = df.sort_values("Month").reset_index(drop=True)

    df = df.rename(
        columns={
            "Month": "month",
            "Sales_Value": "sales_value",
            "MoM_Growth_Percent": "mom_growth_percent",
        }
    )

    df.to_csv(destination, index=False)

    print("\nMONTHLY SALES")
    print(f"Months: {len(df):,}")
    print(f"Output: {destination}")
    print("\nFirst five months:")
    print(df.head().to_string(index=False))


def main() -> None:
    print("=" * 70)
    print("BUILD STANDARDIZED PROJECT OUTPUTS")
    print("=" * 70)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    build_cleaned_transactions()
    build_customer_features()
    build_monthly_sales()

    print("\n" + "=" * 70)
    print("STANDARDIZED OUTPUT GENERATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
