from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "data" / "processed" / "online_retail_prepared.csv"
    output_file = project_root / "reports" / "customer_rfm.csv"

    df = pd.read_csv(
        input_file,
        dtype={"invoiceno": "string", "stockcode": "string"},
    )

    df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")
    df["customerid"] = pd.to_numeric(df["customerid"], errors="coerce")

    # Use only records with an identifiable customer.
    customer_df = df[df["customerid"].notna()].copy()

    # Identify cancellation-style invoices.
    customer_df["is_cancellation"] = (
        customer_df["invoiceno"].str.startswith("C", na=False)
    )

    # Use non-cancellation invoices to calculate purchase frequency,
    # first purchase date, and last observed purchase date.
    regular_df = customer_df[~customer_df["is_cancellation"]].copy()

    purchase_metrics = (
        regular_df.groupby("customerid")
        .agg(
            frequency=("invoiceno", "nunique"),
            first_purchase_date=("invoicedate", "min"),
            last_purchase_date=("invoicedate", "max"),
        )
    )

    # Keep all identifiable-customer transaction values, including
    # negative values, for the initial net monetary measure.
    monetary_metrics = (
        customer_df.groupby("customerid")
        .agg(
            monetary=("line_value", "sum"),
            positive_transaction_value=(
                "line_value",
                lambda values: values[values > 0].sum(),
            ),
        )
    )

    rfm = purchase_metrics.join(monetary_metrics, how="left")

    # Fixed reference date: one day after the dataset's last observed date.
    reference_date = pd.Timestamp("2011-12-10")

    rfm["recency_days"] = (
        reference_date.normalize()
        - rfm["last_purchase_date"].dt.normalize()
    ).dt.days

    rfm["is_repeat_customer"] = rfm["frequency"] >= 2

    rfm = rfm.reset_index().rename(
        columns={"customerid": "customer_id"}
    )

    # Put the most recently purchasing customers first.
    rfm = rfm.sort_values(
        ["recency_days", "frequency"],
        ascending=[True, False],
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    rfm.to_csv(output_file, index=False)

    print("=" * 70)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("RFM CUSTOMER ANALYSIS")
    print("=" * 70)

    print(f"\nReference date: {reference_date.date()}")
    print(f"Identifiable customers with non-cancellation invoices: {len(rfm):,}")
    print(f"Repeat customers: {rfm['is_repeat_customer'].sum():,}")
    print(f"Customers with zero net transaction value: {(rfm['monetary'] == 0).sum():,}")
    print(f"Customers with negative net transaction value: {(rfm['monetary'] < 0).sum():,}")

    print("\nRFM summary:")
    print(
        rfm[["recency_days", "frequency", "monetary"]]
        .describe()
        .round(2)
        .to_string()
    )

    print("\n10 most recently purchasing customers:")
    print(
        rfm[
            [
                "customer_id",
                "recency_days",
                "frequency",
                "monetary",
            ]
        ]
        .head(10)
        .to_string(
            index=False,
            formatters={"monetary": "{:,.2f}".format},
        )
    )

    print(f"\nRFM output saved to:\n{output_file}")
    print("\nRFM analysis completed.")


if __name__ == "__main__":
    main()
