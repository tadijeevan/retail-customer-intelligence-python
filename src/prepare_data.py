from pathlib import Path

import pandas as pd

from src.data_cleaning import prepare_transaction_data


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "online_retail_prepared.csv"
)


def main():
    """Prepare and save the retail transaction dataset."""

    print("=" * 70)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("DATA PREPARATION PIPELINE")
    print("=" * 70)

    # Step 1: Check the source dataset
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATA_PATH}"
        )

    # Step 2: Load the original Excel dataset
    print("\nStep 1: Loading the original dataset...")
    df = pd.read_excel(RAW_DATA_PATH)

    original_rows, original_columns = df.shape

    print(f"Original dataset shape: {df.shape}")

    # Step 3: Prepare the transaction data
    print("\nStep 2: Preparing transaction data...")
    cleaned_df = prepare_transaction_data(df)

    print(f"Prepared dataset shape: {cleaned_df.shape}")

    # Step 4: Display data quality indicators
    print("\nStep 3: Data quality indicators:")

    print(f"Missing customer IDs: {cleaned_df['customerid'].isna().sum():,}")
    print(f"Exact duplicate rows: {cleaned_df.duplicated().sum():,}")
    print(f"Cancellation invoice rows: {cleaned_df['is_cancellation'].sum():,}")
    print(f"Negative quantity rows: {(cleaned_df['quantity'] < 0).sum():,}")
    print(f"Zero unit-price rows: {(cleaned_df['unitprice'] == 0).sum():,}")
    print(f"Negative unit-price rows: {(cleaned_df['unitprice'] < 0).sum():,}")

    # Step 5: Validate the prepared data
    print("\nStep 4: Validating the prepared dataset...")

    if cleaned_df.empty:
        raise ValueError("The prepared dataset is empty.")

    if len(cleaned_df) != original_rows:
        raise ValueError(
            f"Unexpected row-count change: original={original_rows}, "
            f"prepared={len(cleaned_df)}"
        )

    required_columns = {
        "invoiceno",
        "stockcode",
        "invoicedate",
        "quantity",
        "unitprice",
        "customerid",
        "is_cancellation",
        "line_value",
    }

    missing_columns = required_columns.difference(cleaned_df.columns)

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {sorted(missing_columns)}"
        )

    print("Validation passed. All original rows have been retained.")

    # Step 6: Save the prepared dataset
    print("\nStep 5: Saving the prepared dataset...")

    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    cleaned_df.to_csv(
        PROCESSED_DATA_PATH,
        index=False,
    )

    print(f"Saved to: {PROCESSED_DATA_PATH}")

    # Step 7: Display a sample and summary
    print("\nFirst five prepared rows:")
    print(cleaned_df.head().to_string(index=False))

    print("\n" + "=" * 70)
    print("DATA PREPARATION SUMMARY")
    print("=" * 70)
    print(f"Original rows: {original_rows:,}")
    print(f"Prepared rows: {len(cleaned_df):,}")
    print(f"Original columns: {original_columns}")
    print(f"Prepared columns: {len(cleaned_df.columns)}")
    print(f"Total line value: £{cleaned_df['line_value'].sum():,.2f}")
    print("\nOriginal Excel file remains unchanged.")
    print("No rows have been deleted.")
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
