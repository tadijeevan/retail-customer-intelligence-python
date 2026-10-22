from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "online_retail_prepared.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "reports" / "customer_purchase_frequency.csv"
)


def main():
    """Calculate observed invoice frequency for identifiable customers."""

    print("=" * 65)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("CUSTOMER PURCHASE FREQUENCY ANALYSIS")
    print("=" * 65)

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    df["invoicedate"] = pd.to_datetime(
        df["invoicedate"],
        errors="coerce",
    )

    df["invoiceno"] = df["invoiceno"].astype("string")

    # Customer-level analysis requires an identifiable CustomerID.
    customer_df = df[df["customerid"].notna()].copy()

    # Separate cancellation invoices from other invoices.
    customer_df["is_cancellation"] = (
        customer_df["invoiceno"].str.startswith("C", na=False)
    )

    regular_invoices = customer_df[
        ~customer_df["is_cancellation"]
    ].copy()

    cancellation_invoices = customer_df[
        customer_df["is_cancellation"]
    ].copy()

    # Count distinct invoices rather than product transaction rows.
    purchase_frequency = (
        regular_invoices.groupby("customerid")
        .agg(
            purchase_frequency=("invoiceno", "nunique"),
            first_purchase_date=("invoicedate", "min"),
            last_purchase_date=("invoicedate", "max"),
        )
        .reset_index()
    )

    cancellation_frequency = (
        cancellation_invoices.groupby("customerid")
        .agg(
            cancellation_invoice_count=("invoiceno", "nunique"),
        )
        .reset_index()
    )

    customer_summary = purchase_frequency.merge(
        cancellation_frequency,
        on="customerid",
        how="left",
    )

    customer_summary["cancellation_invoice_count"] = (
        customer_summary["cancellation_invoice_count"]
        .fillna(0)
        .astype(int)
    )

    customer_summary["is_repeat_customer"] = (
        customer_summary["purchase_frequency"] >= 2
    )

    # Summarize the distribution of observed invoice frequency.
    frequency_distribution = (
        customer_summary["purchase_frequency"]
        .value_counts()
        .sort_index()
    )

    repeat_customers = customer_summary[
        customer_summary["is_repeat_customer"]
    ]

    print(f"\nTransaction rows loaded: {len(df):,}")
    print(f"Rows with identifiable customers: {len(customer_df):,}")
    print(
        "Identifiable customers with at least one regular invoice: "
        f"{len(customer_summary):,}"
    )
    print(f"Customers with 2+ distinct regular invoices: {len(repeat_customers):,}")

    if len(customer_summary) > 0:
        repeat_percentage = (
            len(repeat_customers) / len(customer_summary)
        ) * 100

        print(f"Observed repeat-customer percentage: {repeat_percentage:.2f}%")

    print("\nPurchase frequency distribution:")
    print("Distinct invoices | Number of customers")

    for invoice_count, customer_count in frequency_distribution.items():
        print(f"{invoice_count:>16} | {customer_count:>18,}")

    print("\nTop 10 customers by observed purchase frequency:")
    print(
        customer_summary.sort_values(
            ["purchase_frequency", "customerid"],
            ascending=[False, True],
        )
        .head(10)
        .to_string(index=False)
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    customer_summary.to_csv(OUTPUT_PATH, index=False)

    print(f"\nCustomer summary saved to: {OUTPUT_PATH}")
    print("\nCustomer purchase frequency analysis completed.")


if __name__ == "__main__":
    main()
