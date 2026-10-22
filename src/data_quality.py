from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path.cwd()
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def main():
    """Investigate missing customer IDs in the Online Retail dataset."""

    print("=" * 60)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("DATA QUALITY INVESTIGATION")
    print("=" * 60)

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATA_PATH}")

    print("\nLoading the original dataset...")
    df = pd.read_excel(RAW_DATA_PATH)

    total_rows = len(df)
    missing_customer_rows = df["CustomerID"].isna().sum()
    available_customer_rows = df["CustomerID"].notna().sum()

    missing_percentage = missing_customer_rows / total_rows * 100
    available_percentage = available_customer_rows / total_rows * 100

    print("\n1. CUSTOMER ID COMPLETENESS")
    print("-" * 40)
    print(f"Total transaction rows: {total_rows:,}")
    print(f"Rows with missing CustomerID: {missing_customer_rows:,}")
    print(f"Rows with available CustomerID: {available_customer_rows:,}")
    print(f"Percentage with missing CustomerID: {missing_percentage:.2f}%")
    print(f"Percentage with available CustomerID: {available_percentage:.2f}%")

    print("\n2. TRANSACTION VALUE COMPARISON")
    print("-" * 40)

    df["LineValue"] = df["Quantity"] * df["UnitPrice"]

    df["CustomerID_Status"] = df["CustomerID"].isna().map(
        {
            True: "Missing CustomerID",
            False: "CustomerID Available",
        }
    )

    comparison = (
        df.groupby("CustomerID_Status")
        .agg(
            Transaction_Rows=("InvoiceNo", "size"),
            Total_Quantity=("Quantity", "sum"),
            Total_Line_Value=("LineValue", "sum"),
        )
        .reset_index()
    )

    print(
        comparison.to_string(
            index=False,
            formatters={"Total_Line_Value": "{:,.2f}".format},
        )
    )

    print("\n3. INITIAL INTERPRETATION")
    print("-" * 40)
    print(
        "Transactions without CustomerID may still be useful "
        "for aggregate sales analysis."
    )
    print(
        "They cannot be reliably assigned to individual customers "
        "for RFM segmentation."
    )
    print(
        "The original Excel file has not been modified, "
        "and no rows have been deleted."
    )


if __name__ == "__main__":
    main()
