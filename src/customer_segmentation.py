from pathlib import Path

import pandas as pd


def assign_segment(row):
    r = row["R_score"]
    f = row["F_score"]
    m = row["M_score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    elif r >= 3 and f >= 4:
        return "Loyal Customers"

    elif r >= 4 and f <= 2:
        return "Recent Customers"

    elif m == 5:
        return "High-Spending Customers"

    elif r <= 2 and (f >= 2 or m >= 4):
        return "Needs Attention"

    elif r <= 2 and f <= 2 and m <= 2:
        return "Low-Activity Customers"

    else:
        return "Other Customers"


def main():
    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "reports" / "customer_rfm_scored.csv"
    customer_output = project_root / "reports" / "customer_segments.csv"
    summary_output = project_root / "reports" / "customer_segment_summary.csv"

    df = pd.read_csv(input_file)

    required_columns = [
        "customer_id",
        "R_score",
        "F_score",
        "M_score",
    ]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df[required_columns].isna().any().any():
        raise ValueError("Missing values found in required segmentation columns.")

    df["segment"] = df.apply(assign_segment, axis=1)

    total_customers = len(df)

    summary = (
        df.groupby("segment")
        .agg(
            customer_count=("customer_id", "nunique"),
            average_recency_days=("recency_days", "mean"),
            average_purchase_frequency=("frequency", "mean"),
            average_monetary=("monetary", "mean"),
            median_monetary=("monetary", "median"),
        )
        .reset_index()
    )

    summary["customer_percentage"] = (
        summary["customer_count"] / total_customers * 100
    )

    summary = summary.sort_values(
        "customer_count", ascending=False
    )

    df.to_csv(customer_output, index=False)
    summary.to_csv(summary_output, index=False)

    print("=" * 70)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("CUSTOMER SEGMENTATION")
    print("=" * 70)

    print(f"\nTotal customers segmented: {total_customers:,}")

    print("\nCustomer segment summary:")
    print(
        summary.to_string(
            index=False,
            formatters={
                "average_recency_days": "{:.1f}".format,
                "average_purchase_frequency": "{:.2f}".format,
                "average_monetary": "{:,.2f}".format,
                "median_monetary": "{:,.2f}".format,
                "customer_percentage": "{:.2f}%".format,
            },
        )
    )

    print(
        "\nCustomer-level segments saved to:\n"
        f"{customer_output}"
    )
    print(
        "\nSegment summary saved to:\n"
        f"{summary_output}"
    )

    print("\nCustomer segmentation completed.")


if __name__ == "__main__":
    main()
