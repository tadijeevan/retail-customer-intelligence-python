from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"

INPUT_PATH = PROCESSED_DIR / "customer_clustering_features.csv"
SEGMENTS_PATH = REPORTS_DIR / "customer_segments.csv"

ASSIGNMENTS_PATH = REPORTS_DIR / "customer_cluster_assignments.csv"
SUMMARY_PATH = REPORTS_DIR / "customer_cluster_profiles.csv"

FEATURE_COLUMNS = [
    "recency_log_scaled",
    "frequency_log_scaled",
    "positive_value_log_scaled",
    "distinct_products_log_scaled",
]

RAW_FEATURE_COLUMNS = [
    "recency_days",
    "frequency",
    "positive_transaction_value",
    "distinct_products",
]

N_CLUSTERS = 2
RANDOM_STATE = 42


def main() -> None:
    print("=" * 70)
    print("CUSTOMER CLUSTERING — FINALIST PROFILE")
    print("=" * 70)

    df = pd.read_csv(INPUT_PATH)
    rfm_segments = pd.read_csv(SEGMENTS_PATH)

    if df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs in clustering dataset.")

    if rfm_segments["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs in RFM segment dataset.")

    model = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_STATE,
        n_init=20,
    )

    labels = model.fit_predict(df[FEATURE_COLUMNS])

    assignments = df[
        ["customer_id"] + RAW_FEATURE_COLUMNS
    ].copy()

    assignments["cluster"] = labels

    # Attach the existing rule-based RFM segment for comparison.
    assignments = assignments.merge(
        rfm_segments[["customer_id", "segment"]],
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    if len(assignments) != len(df):
        raise ValueError("Customer count changed during cluster assignment.")

    if assignments["cluster"].isna().any():
        raise ValueError("Some customers have no cluster assignment.")

    assignments["cluster"] = assignments["cluster"].astype(int)

    summary = (
        assignments.groupby("cluster")
        .agg(
            customer_count=("customer_id", "count"),
            avg_recency_days=("recency_days", "mean"),
            median_recency_days=("recency_days", "median"),
            avg_frequency=("frequency", "mean"),
            median_frequency=("frequency", "median"),
            avg_positive_transaction_value=(
                "positive_transaction_value",
                "mean",
            ),
            median_positive_transaction_value=(
                "positive_transaction_value",
                "median",
            ),
            avg_distinct_products=("distinct_products", "mean"),
            median_distinct_products=("distinct_products", "median"),
        )
        .reset_index()
    )

    summary["customer_percentage"] = (
        summary["customer_count"] / len(assignments) * 100
    )

    assignments.to_csv(ASSIGNMENTS_PATH, index=False)
    summary.to_csv(SUMMARY_PATH, index=False)

    print(f"\nCustomers assigned: {len(assignments):,}")
    print(f"Clusters: {N_CLUSTERS}")

    print("\nCluster profiles:")
    print(summary.round(2).to_string(index=False))

    print("\nExisting RFM segments within each cluster:")
    print(
        pd.crosstab(
            assignments["cluster"],
            assignments["segment"],
            normalize="index",
        )
        .mul(100)
        .round(1)
        .to_string()
    )

    print(f"\nCustomer assignments saved to:\n{ASSIGNMENTS_PATH}")
    print(f"\nCluster profiles saved to:\n{SUMMARY_PATH}")

    print(
        "\nThese clusters are data-driven groups. "
        "Interpret their business meaning from the observed profiles "
        "rather than assigning labels in advance."
    )


if __name__ == "__main__":
    main()
