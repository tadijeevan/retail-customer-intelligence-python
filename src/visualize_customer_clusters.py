from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

PROFILE_PATH = REPORTS_DIR / "customer_cluster_profiles.csv"
OUTPUT_PATH = FIGURES_DIR / "cluster_profiles.png"


def main() -> None:
    print("=" * 70)
    print("CUSTOMER CLUSTER PROFILE VISUALIZATION")
    print("=" * 70)

    profiles = pd.read_csv(PROFILE_PATH)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    metrics = [
        ("avg_recency_days", "Average Recency (Days)"),
        ("avg_frequency", "Average Purchase Frequency"),
        (
            "avg_positive_transaction_value",
            "Average Positive Transaction Value (£)",
        ),
        ("avg_distinct_products", "Average Distinct Products"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axes = axes.flatten()

    for ax, (column, title) in zip(axes, metrics):
        ax.bar(
            profiles["cluster"].astype(str),
            profiles[column],
        )
        ax.set_title(title)
        ax.set_xlabel("Cluster")
        ax.set_ylabel(title)
        ax.grid(axis="y", alpha=0.3)

    fig.suptitle(
        "Customer Cluster Profiles — K-Means (K=2)",
        fontsize=15,
    )
    fig.tight_layout()

    fig.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"\nCluster profile chart saved to:\n{OUTPUT_PATH}")
    print("Visualization completed successfully.")


if __name__ == "__main__":
    main()
