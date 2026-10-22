from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path.cwd()
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def main():
    """Inspect repeated invoice-product combinations."""

    df = pd.read_excel(RAW_DATA_PATH)

    invoice_number = "555524"

    selected = df.loc[
        (df["InvoiceNo"].astype("string") == invoice_number)
        & (df["StockCode"].astype("string").isin(["22698", "22697"]))
    ].copy()

    print("=" * 60)
    print(f"INVESTIGATION OF INVOICE {invoice_number}")
    print("=" * 60)

    print(f"\nSelected transaction rows: {len(selected)}")
    print(f"Exact duplicate rows within selected records: "
          f"{selected.duplicated().sum()}")

    print("\nTransaction details:")
    print(selected.to_string(index=False))

    print("\nSummary by product:")
    summary = (
        selected.groupby("StockCode")
        .agg(
            Transaction_Rows=("InvoiceNo", "size"),
            Total_Quantity=("Quantity", "sum"),
            Unit_Prices=("UnitPrice", "nunique"),
            Descriptions=("Description", "nunique"),
        )
        .reset_index()
    )

    print(summary.to_string(index=False))

    print("\nOriginal Excel file has not been modified.")


if __name__ == "__main__":
    main()
