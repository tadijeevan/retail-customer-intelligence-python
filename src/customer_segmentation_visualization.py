from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "reports" / "customer_segment_summary.csv"
    figures_dir = project_root / "reports" / "figures"

    figures_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_file)

    required_columns = [
        "segment",
        "customer_count",
        "average_monetary",
        "average_recency_days",
    ]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Chart 1: Number of customers in each segment.
    customer_counts = df.sort_values("customer_count", ascending=False)

    plt.figure(figsize=(11, 6))
    plt.bar(customer_counts["segment"], customer_counts["customer_count"])
    plt.title("Customer Count by Segment")
    plt.xlabel("Customer Segment")
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()

    count_path = figures_dir / "customer_count_by_segment.png"
    plt.savefig(count_path, dpi=300, bbox_inches="tight")
    plt.close()

    # Chart 2: Average net transaction line value by segment.
    monetary = df.sort_values("average_monetary", ascending=False)

    plt.figure(figsize=(11, 6))
    plt.bar(monetary["segment"], monetary["average_monetary"])
    plt.title("Average Net Transaction Line Value by Segment")
    plt.xlabel("Customer Segment")
    plt.ylabel("Average Value (£)")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()

    monetary_path = figures_dir / "average_monetary_by_segment.png"
    plt.savefig(monetary_path, dpi=300, bbox_inches="tight")
    plt.close()

    # Chart 3: Average recency by segment.
    recency = df.sort_values("average_recency_days", ascending=True)

    plt.figure(figsize=(11, 6))
    plt.bar(recency["segment"], recency["average_recency_days"])
    plt.title("Average Recency by Customer Segment")
    plt.xlabel("Customer Segment")
    plt.ylabel("Average Days Since Last Observed Purchase")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()

    recency_path = figures_dir / "average_recency_by_segment.png"
    plt.savefig(recency_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("=" * 70)
    print("CUSTOMER SEGMENTATION VISUALIZATION")
    print("=" * 70)
    print(f"\nInput file: {input_file}")
    print("\nCharts created successfully:")

    for path in [count_path, monetary_path, recency_path]:
        print(f"- {path}")

    print("\nVisualization completed.")


if __name__ == "__main__":
    main()
