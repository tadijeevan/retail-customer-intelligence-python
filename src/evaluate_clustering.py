from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_clustering_features.csv"
)
OUTPUT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "clustering_model_evaluation.csv"
)

FEATURE_COLUMNS = [
    "recency_log_scaled",
    "frequency_log_scaled",
    "positive_value_log_scaled",
    "distinct_products_log_scaled",
]

CLUSTER_COUNTS = range(2, 9)
RANDOM_STATE = 42


def main() -> None:
    print("=" * 70)
    print("K-MEANS CLUSTER COUNT EVALUATION")
    print("=" * 70)

    df = pd.read_csv(INPUT_PATH)
    X = df[FEATURE_COLUMNS]

    if X.isna().any().any():
        raise ValueError("Missing values found in clustering features.")

    results = []

    for k in CLUSTER_COUNTS:
        print(f"\nEvaluating K = {k} ...")

        model = KMeans(
            n_clusters=k,
            random_state=RANDOM_STATE,
            n_init=20,
        )

        labels = model.fit_predict(X)

        score = silhouette_score(
            X,
            labels,
            sample_size=min(2000, len(X)),
            random_state=RANDOM_STATE,
        )

        cluster_sizes = pd.Series(labels).value_counts()

        results.append(
            {
                "n_clusters": k,
                "inertia": model.inertia_,
                "silhouette_score": score,
                "smallest_cluster_size": int(cluster_sizes.min()),
                "largest_cluster_size": int(cluster_sizes.max()),
            }
        )

        print(f"Inertia: {model.inertia_:.2f}")
        print(f"Silhouette score: {score:.4f}")
        print(f"Smallest cluster: {cluster_sizes.min():,} customers")
        print(f"Largest cluster: {cluster_sizes.max():,} customers")

    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_PATH, index=False)

    print("\n" + "=" * 70)
    print("MODEL EVALUATION SUMMARY")
    print("=" * 70)

    print(
        results_df.sort_values(
            "n_clusters"
        ).round(4).to_string(index=False)
    )

    best_row = results_df.loc[
        results_df["silhouette_score"].idxmax()
    ]

    print("\nHighest sampled silhouette score:")
    print(f"K = {int(best_row['n_clusters'])}")
    print(f"Score = {best_row['silhouette_score']:.4f}")

    print(f"\nEvaluation report saved to:\n{OUTPUT_PATH}")

    print(
        "\nImportant: The highest silhouette score is a diagnostic, "
        "not an automatic final model selection. We must also examine "
        "cluster sizes, profiles, and business usefulness."
    )


if __name__ == "__main__":
    main()
