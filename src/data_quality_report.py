from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path.cwd()
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
REPORT_PATH = PROJECT_ROOT / "reports" / "data_quality_report.csv"


def main():
    """Generate a consolidated data quality report."""

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATA_PATH}")

    df = pd.read_excel(RAW_DATA_PATH)

    cancellation_mask = (
        df["InvoiceNo"].astype("string").str.startswith("C", na=False)
    )

    parsed_dates = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    metrics = [
        ("Total transaction rows", len(df)),
        ("Exact duplicate rows", int(df.duplicated().sum())),
        ("Missing customer IDs", int(df["CustomerID"].isna().sum())),
        ("Missing descriptions", int(df["Description"].isna().sum())),
        ("Cancellation-style invoice rows", int(cancellation_mask.sum())),
        ("Negative quantity rows", int((df["Quantity"] < 0).sum())),
        ("Zero quantity rows", int((df["Quantity"] == 0).sum())),
        ("Zero unit-price rows", int((df["UnitPrice"] == 0).sum())),
        ("Negative unit-price rows", int((df["UnitPrice"] < 0).sum())),
        ("Missing invoice dates", int(df["InvoiceDate"].isna().sum())),
        ("Missing or unparseable invoice dates", int(parsed_dates.isna().sum())),
    ]

    report = pd.DataFrame(metrics, columns=["Metric", "Value"])
    report["Percentage_of_Rows"] = (
        report["Value"] / len(df) * 100
    ).round(2)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(REPORT_PATH, index=False)

    print("=" * 60)
    print("CONSOLIDATED DATA QUALITY REPORT")
    print("=" * 60)
    print(report.to_string(index=False))
    print(f"\nReport saved to: {REPORT_PATH}")
    print("The original Excel file has not been modified.")


if __name__ == "__main__":
    main()
