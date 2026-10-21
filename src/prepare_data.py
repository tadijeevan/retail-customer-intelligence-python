from pathlib import Path

import pandas as pd

from src.data_cleaning import prepare_transaction_data


# Define project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def main():
    """Load the raw dataset, prepare it, and display a summary."""

    print("=" * 60)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("DATA PREPARATION")
    print("=" * 60)

    # Verify that the dataset exists
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_PATH}\n"
            "Ensure Online Retail.xlsx is inside data/raw/."
        )

    # Load the original dataset
    print("\nStep 1: Loading the original dataset...")
    df = pd.read_excel(RAW_DATA_PATH)

    print(f"Original dataset shape: {df.shape}")

    # Apply the existing data-cleaning functions
    print("\nStep 2: Preparing transaction data...")
    cleaned_df = prepare_transaction_data(df)

    print("Data preparation completed successfully.")
    print(f"Prepared dataset shape: {cleaned_df.shape}")

    # Display standardized column names
    print("\nStep 3: Prepared column names:")
    print(cleaned_df.columns.tolist())

    # Display data types
    print("\nStep 4: Prepared data types:")
    print(cleaned_df.dtypes.to_string())

    # Display missing values
    print("\nStep 5: Missing values by column:")
    print(cleaned_df.isna().sum().to_string())

    # Count cancellation-style invoices
    cancellation_count = cleaned_df["is_cancellation"].sum()
    print(f"\nCancellation-style invoice rows: {cancellation_count:,}")

    # Count negative quantities
    negative_quantity_count = (cleaned_df["quantity"] < 0).sum()
    print(f"Rows with negative quantities: {negative_quantity_count:,}")

    # Count non-positive prices
    non_positive_price_count = (cleaned_df["unitprice"] <= 0).sum()
    print(f"Rows with non-positive unit prices: {non_positive_price_count:,}")

    # Display the first five prepared rows
    print("\nStep 6: First five prepared rows:")
    print(cleaned_df.head().to_string(index=False))

    print("\n" + "=" * 60)
    print("DATA PREPARATION SUMMARY")
    print("=" * 60)
    print("The original Excel file has not been modified.")
    print("The prepared DataFrame exists in memory only.")
    print("No rows have been deleted.")
    print("No processed dataset has been saved yet.")


if __name__ == "__main__":
    main()
