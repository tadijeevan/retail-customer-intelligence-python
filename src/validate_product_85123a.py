from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
data_path = project_root / "data" / "processed" / "online_retail_prepared.csv"

df = pd.read_csv(data_path)

df["stockcode"] = df["stockcode"].astype("string").str.strip().str.upper()

product = df[df["stockcode"] == "85123A"].copy()

print("=" * 65)
print("VALIDATION: PRODUCT 85123A")
print("=" * 65)

print(f"Total rows: {len(product):,}")

checks = {
    "All rows": pd.Series(True, index=product.index),
    "Positive quantity and positive price": (
        (product["quantity"] > 0) & (product["unitprice"] > 0)
    ),
    "Not a cancellation invoice": ~product["is_cancellation"].astype(bool),
    "Positive quantity, positive price, not cancellation": (
        (product["quantity"] > 0)
        & (product["unitprice"] > 0)
        & (~product["is_cancellation"].astype(bool))
    ),
}

for label, mask in checks.items():
    selected = product[mask]
    print(f"\n{label}")
    print(f"  Rows: {len(selected):,}")
    print(f"  Positive line value: £{selected.loc[selected['line_value'] > 0, 'line_value'].sum():,.2f}")
    print(f"  Negative line value: £{selected.loc[selected['line_value'] < 0, 'line_value'].sum():,.2f}")
    print(f"  Net line value: £{selected['line_value'].sum():,.2f}")

print("\nRows with positive line value but non-positive quantity or price:")
unusual = product[
    (product["line_value"] > 0)
    & ((product["quantity"] <= 0) | (product["unitprice"] <= 0))
]

print(
    unusual[
        [
            "invoiceno",
            "quantity",
            "unitprice",
            "line_value",
            "is_cancellation",
        ]
    ].head(20).to_string(index=False)
)

print("\nValidation completed.")
