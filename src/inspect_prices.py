from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path.cwd()
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def main():
    """Investigate zero and negative unit prices."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATA_PATH}")

    df = pd.read_excel(RAW_DATA_PATH)

    zero_prices = df[df["UnitPrice"] == 0].copy()
    negative_prices = df[df["UnitPrice"] < 0].copy()

    print("=" * 60)
    print("UNIT PRICE INVESTIGATION")
    print("=" * 60)

    print(f"\nTotal transaction rows: {len(df):,}")
    print(f"Rows with zero unit price: {len(zero_prices):,}")
    print(f"Rows with negative unit price: {len(negative_prices):,}")

    print("\n1. ZERO-PRICE TRANSACTION SUMMARY")
    print("-" * 40)

    print(f"Missing descriptions: {zero_prices['Description'].isna().sum():,}")
    print(f"Missing customer IDs: {zero_prices['CustomerID'].isna().sum():,}")

    cancellation_count = (
        zero_prices["InvoiceNo"]
        .astype("string")
        .str.startswith("C", na=False)
        .sum()
    )

    print(f"Cancellation-style invoices: {cancellation_count:,}")

    print("\nFirst 10 zero-price records:")
    print(zero_prices.head(10).to_string(index=False))

    print("\n2. NEGATIVE-PRICE RECORDS")
    print("-" * 40)

    if negative_prices.empty:
        print("No negative-price records found.")
    else:
        print(negative_prices.to_string(index=False))

    print("\n3. INITIAL INTERPRETATION")
    print("-" * 40)
    print(
        "Zero-price records contribute zero to line revenue when "
        "quantity is multiplied by unit price."
    )
    print(
        "Negative-price records require individual inspection "
        "before deciding how to handle them."
    )
    print("The original Excel file has not been modified.")


if __name__ == "__main__":
    main()
