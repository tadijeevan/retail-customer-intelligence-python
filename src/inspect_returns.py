from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path.cwd()
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def main():
    """Investigate negative quantities and cancellation invoices."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATA_PATH}")

    df = pd.read_excel(RAW_DATA_PATH)

    df["Is_Cancellation"] = (
        df["InvoiceNo"].astype("string").str.startswith("C", na=False)
    )
    df["Has_Negative_Quantity"] = df["Quantity"] < 0
    df["LineValue"] = df["Quantity"] * df["UnitPrice"]

    print("=" * 65)
    print("NEGATIVE QUANTITY AND CANCELLATION INVESTIGATION")
    print("=" * 65)
    print(f"\nTotal transaction rows: {len(df):,}")

    print("\n1. NEGATIVE QUANTITY AND CANCELLATION COMPARISON")
    print("-" * 50)

    comparison = pd.crosstab(
        df["Has_Negative_Quantity"],
        df["Is_Cancellation"],
        rownames=["Negative quantity"],
        colnames=["Cancellation invoice"],
        margins=True,
    )
    print(comparison.to_string())

    negative_rows = df[df["Has_Negative_Quantity"]]

    print("\n2. NEGATIVE QUANTITY ROWS BY INVOICE TYPE")
    print("-" * 50)

    summary = (
        negative_rows.groupby("Is_Cancellation")
        .agg(
            Transaction_Rows=("InvoiceNo", "size"),
            Total_Quantity=("Quantity", "sum"),
            Total_Line_Value=("LineValue", "sum"),
        )
        .reset_index()
    )

    summary["Invoice_Type"] = summary["Is_Cancellation"].map(
        {
            True: "Cancellation-style invoice",
            False: "Other invoice format",
        }
    )

    print(
        summary[
            [
                "Invoice_Type",
                "Transaction_Rows",
                "Total_Quantity",
                "Total_Line_Value",
            ]
        ].to_string(
            index=False,
            formatters={"Total_Line_Value": "{:,.2f}".format},
        )
    )

    columns_to_show = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "UnitPrice",
        "LineValue",
        "CustomerID",
    ]

    print("\n3. NEGATIVE QUANTITIES WITH CANCELLATION INVOICES")
    print("-" * 50)
    print(
        negative_rows.loc[
            negative_rows["Is_Cancellation"], columns_to_show
        ].head(10).to_string(index=False)
    )

    print("\n4. NEGATIVE QUANTITIES WITHOUT CANCELLATION INVOICES")
    print("-" * 50)
    print(
        negative_rows.loc[
            ~negative_rows["Is_Cancellation"], columns_to_show
        ].head(10).to_string(index=False)
    )

    print("\nInvestigation complete. No rows have been deleted.")


if __name__ == "__main__":
    main()
