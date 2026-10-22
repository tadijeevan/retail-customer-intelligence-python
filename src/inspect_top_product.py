from pathlib import Path

import pandas as pd


project_root = Path.cwd()
data_path = (
    project_root / "data" / "processed" / "online_retail_prepared.csv"
)

df = pd.read_csv(data_path)

target_code = "23843"

product_rows = df[df["stockcode"].astype(str) == target_code].copy()

print("=" * 70)
print("PRODUCT INVESTIGATION: PAPER CRAFT, LITTLE BIRDIE")
print("=" * 70)

print(f"\nMatching transaction rows: {len(product_rows):,}")

if product_rows.empty:
    print("No records found for this product code.")
else:
    print("\nMatching records:")
    print(
        product_rows[
            [
                "invoiceno",
                "stockcode",
                "description",
                "quantity",
                "invoicedate",
                "unitprice",
                "customerid",
                "country",
                "is_cancellation",
                "line_value",
            ]
        ].to_string(index=False)
    )

    print("\nSummary:")
    print(f"Total quantity: {product_rows['quantity'].sum():,.0f}")
    print(f"Total line value: £{product_rows['line_value'].sum():,.2f}")
    print(f"Unique invoice numbers: {product_rows['invoiceno'].nunique():,}")
    print(f"Unique descriptions: {product_rows['description'].nunique()}")

print("\n" + "=" * 70)
