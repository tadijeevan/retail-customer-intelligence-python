from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "data" / "processed" / "online_retail_prepared.csv"
    output_file = project_root / "reports" / "customer_spending_analysis.csv"

    df = pd.read_csv(
        input_file,
        dtype={"invoiceno": "string", "stockcode": "string"},
    )

    df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")
    df["customerid"] = pd.to_numeric(df["customerid"], errors="coerce")

    # Customer-level analysis requires an identifiable CustomerID.
    customer_df = df[df["customerid"].notna()].copy()

    # Exclude cancellation-style invoices from purchase frequency and
    # first/last purchase dates. Keep all rows for value and quantity metrics.
    customer_df["is_cancellation"] = (
        customer_df["invoiceno"].str.startswith("C", na=False)
    )

    regular_df = customer_df[~customer_df["is_cancellation"]].copy()

    # Purchase frequency and dates based on non-cancellation invoices.
    purchase_metrics = (
        regular_df.groupby("customerid")
        .agg(
            purchase_frequency=("invoiceno", "nunique"),
            first_purchase_date=("invoicedate", "min"),
            last_purchase_date=("invoicedate", "max"),
        )
    )

    # Spending, quantity and product metrics retain negative transaction
    # values so that returns and reversals are not silently discarded.
    value_metrics = (
        customer_df.groupby("customerid")
        .agg(
            total_transaction_value=("line_value", "sum"),
            positive_transaction_value=(
                "line_value",
                lambda values: values[values > 0].sum(),
            ),
            total_units_net=("quantity", "sum"),
            distinct_products=("stockcode", "nunique"),
        )
    )

    customer_summary = purchase_metrics.join(value_metrics, how="left")

    customer_summary["is_repeat_customer"] = (
        customer_summary["purchase_frequency"] >= 2
    )

    customer_summary = customer_summary.reset_index()
    customer_summary = customer_summary.rename(
        columns={"customerid": "customer_id"}
    )

    customer_summary = customer_summary.sort_values(
        "total_transaction_value", ascending=False
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    customer_summary.to_csv(output_file, index=False)

    print("=" * 70)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("CUSTOMER SPENDING ANALYSIS")
    print("=" * 70)

    print(f"\nIdentifiable customers analysed: {len(customer_summary):,}")
    print(
        "Customers with at least one non-cancellation invoice: "
        f"{customer_summary['purchase_frequency'].notna().sum():,}"
    )
    print(
        "Customers with 2+ distinct non-cancellation invoices: "
        f"{customer_summary['is_repeat_customer'].sum():,}"
    )

    print("\nTop 10 customers by total transaction line value:")
    display_columns = [
        "customer_id",
        "purchase_frequency",
        "total_transaction_value",
        "positive_transaction_value",
        "total_units_net",
        "distinct_products",
    ]

    print(
        customer_summary[display_columns]
        .head(10)
        .to_string(index=False, formatters={
            "total_transaction_value": "{:,.2f}".format,
            "positive_transaction_value": "{:,.2f}".format,
        })
    )

    print(f"\nCustomer spending summary saved to:\n{output_file}")
    print("\nCustomer spending analysis completed.")


if __name__ == "__main__":
    main()
