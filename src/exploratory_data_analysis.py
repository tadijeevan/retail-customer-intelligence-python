from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "online_retail_prepared.csv"
)


def main():
    """Explore the overall structure of the retail dataset."""

    print("=" * 65)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 65)

    # Step 1: Verify the prepared dataset exists
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Prepared dataset not found: {PROCESSED_DATA_PATH}"
        )

    # Step 2: Load the prepared dataset
    print("\nStep 1: Loading prepared dataset...")

    df = pd.read_csv(
        PROCESSED_DATA_PATH,
        parse_dates=["invoicedate"],
    )

    print(f"Dataset shape: {df.shape}")

    # Step 3: Calculate overall business metrics
    print("\nStep 2: Overall business metrics")

    total_rows = len(df)
    unique_invoices = df["invoiceno"].nunique()
    unique_products = df["stockcode"].nunique()
    identifiable_customers = df["customerid"].nunique()
    unique_countries = df["country"].nunique()

    first_invoice_date = df["invoicedate"].min()
    last_invoice_date = df["invoicedate"].max()

    total_line_value = df["line_value"].sum()

    print(f"Total transaction rows: {total_rows:,}")
    print(f"Unique invoice numbers: {unique_invoices:,}")
    print(f"Unique product codes: {unique_products:,}")
    print(f"Identifiable customers: {identifiable_customers:,}")
    print(f"Unique countries: {unique_countries:,}")

    print(f"First invoice date: {first_invoice_date:%Y-%m-%d}")
    print(f"Last invoice date: {last_invoice_date:%Y-%m-%d}")

    print(f"Total line value: £{total_line_value:,.2f}")

    # Step 4: Top 10 countries by transaction rows
    print("\nStep 3: Top 10 countries by transaction rows")

    country_summary = (
        df.groupby("country")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    print(country_summary.to_string())

    # Step 5: Five most frequently occurring product codes
    print("\nStep 4: Five most frequently occurring product codes")

    product_summary = (
        df.groupby("stockcode")
        .size()
        .sort_values(ascending=False)
        .head(5)
    )

    print(product_summary.to_string())

    print("\n" + "=" * 65)
    print("EXPLORATORY DATA ANALYSIS COMPLETED")
    print("=" * 65)


if __name__ == "__main__":
    main()
