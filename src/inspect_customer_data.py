from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
data_path = project_root / "data" / "processed" / "online_retail_prepared.csv"

df = pd.read_csv(data_path)

print("=" * 60)
print("CUSTOMER DATA INSPECTION")
print("=" * 60)

print(f"\nTotal transaction rows: {len(df):,}")
print(f"Rows with CustomerID: {df['customerid'].notna().sum():,}")
print(f"Rows without CustomerID: {df['customerid'].isna().sum():,}")
print(f"Unique identifiable customers: {df['customerid'].nunique():,}")

print("\nSample customer transactions:")
print(
    df.loc[
        df["customerid"].notna(),
        [
            "invoiceno",
            "invoicedate",
            "customerid",
            "stockcode",
            "quantity",
            "unitprice",
            "line_value",
            "is_cancellation",
        ],
    ].head(10).to_string(index=False)
)

print("\nCustomer transaction date range:")
print(f"First invoice date: {df['invoicedate'].min()}")
print(f"Last invoice date:  {df['invoicedate'].max()}")
