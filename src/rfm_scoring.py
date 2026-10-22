from pathlib import Path

import pandas as pd


def assign_quantile_scores(series, higher_is_better=True):
    """
    Assign scores from 1 to 5 using percentile ranks.

    Higher scores represent better results according to the metric.
    Rank-based scoring also handles tied values without requiring
    five distinct values in every metric.
    """
    percentile = series.rank(method="average", pct=True)

    if higher_is_better:
        scores = (percentile * 5).apply(lambda value: min(5, int(value) + 1))
    else:
        scores = ((1 - percentile) * 5).apply(
            lambda value: min(5, int(value) + 1)
        )

    return scores.astype(int)


def main():
    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "reports" / "customer_rfm.csv"
    output_file = project_root / "reports" / "customer_rfm_scored.csv"

    rfm = pd.read_csv(input_file)

    required_columns = [
        "customer_id",
        "recency_days",
        "frequency",
        "monetary",
    ]

    missing_columns = [
        column for column in required_columns if column not in rfm.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if rfm[required_columns].isna().any().any():
        raise ValueError("Missing values found in required RFM columns.")

    # Recency: fewer days since the last purchase is better.
    rfm["R_score"] = assign_quantile_scores(
        rfm["recency_days"], higher_is_better=False
    )

    # Frequency: more distinct invoices is better.
    rfm["F_score"] = assign_quantile_scores(
        rfm["frequency"], higher_is_better=True
    )

    # Monetary: higher net transaction value receives a higher score.
    # Negative values remain unchanged and may receive low scores.
    rfm["M_score"] = assign_quantile_scores(
        rfm["monetary"], higher_is_better=True
    )

    rfm["RFM_score"] = (
        rfm["R_score"].astype(str)
        + rfm["F_score"].astype(str)
        + rfm["M_score"].astype(str)
    )

    rfm["RFM_total_score"] = (
        rfm["R_score"] + rfm["F_score"] + rfm["M_score"]
    )

    rfm.to_csv(output_file, index=False)

    print("=" * 70)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("RFM SCORING")
    print("=" * 70)

    print(f"\nCustomers scored: {len(rfm):,}")

    print("\nScore distributions:")
    for column in ["R_score", "F_score", "M_score"]:
        print(f"\n{column}:")
        print(rfm[column].value_counts().sort_index().to_string())

    print("\nMost common RFM scores:")
    print(rfm["RFM_score"].value_counts().head(10).to_string())

    print("\nTop 10 customers by combined RFM score:")
    print(
        rfm.sort_values(
            ["RFM_total_score", "monetary"],
            ascending=[False, False],
        )[
            [
                "customer_id",
                "recency_days",
                "frequency",
                "monetary",
                "R_score",
                "F_score",
                "M_score",
                "RFM_score",
                "RFM_total_score",
            ]
        ].head(10).to_string(index=False)
    )

    print(f"\nScored RFM data saved to:\n{output_file}")
    print("\nRFM scoring completed.")


if __name__ == "__main__":
    main()
