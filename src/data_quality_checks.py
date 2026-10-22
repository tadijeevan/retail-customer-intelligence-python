from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path.cwd()
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"


def main():
    print("=" * 60)
    print("DATA QUALITY CHECKS")
    print("=" * 60)

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATA_PATH}")

    df = pd.read_excel(RAW_DATA_PATH)

    checks = {
        "Total transaction rows": len(df),
        "Exact duplicate rows": df.duplicated().sum(),
        "Cancellation invoices": (
            df["InvoiceNo"].astype("string").str.startswith("C", na=False).sum()
        ),
        "Negative quantities": (df["Quantity"] < 0).sum(),
        "Zero quantities": (df["Quantity"] == 0).sum(),
        "Zero unit prices": (df["UnitPrice"] == 0).sum(),
        "Negative unit prices": (df["UnitPrice"] < 0).sum(),
        "Missing descriptions": df["Description"].isna().sum(),
        "Missing invoice dates": df["InvoiceDate"].isna().sum(),
        "Invalid invoice dates": (
            pd.to_datetime(df["InvoiceDate"], errors="coerce").isna().sum()
        ),
    }

    print("\nDATA QUALITY RESULTS")
    print("-" * 40)

    for check_name, result in checks.items():
        print(f"{check_name}: {result:,}")

    print("\nInvestigation complete.")
    print("The original Excel file has not been modified.")


if __name__ == "__main__":
    main()
