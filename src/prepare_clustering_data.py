from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"

FEATURE_COLUMNS = [
    "recency_days",
    "frequency",
    "positive_transaction_value",
    "distinct_products",
]


def main() -> None:
    print("=" * 70)
    print("CUSTOMER CLUSTERING — FEATURE PREPARATION")
    print("=" * 70)

    customer_features_path = PROCESSED_DIR / "customer_features.csv"
    rfm_path = REPORTS_DIR / "customer_rfm.csv"

    output_path = PROCESSED_DIR / "customer_clustering_features.csv"
    audit_path = REPORTS_DIR / "clustering_feature_summary.csv"

    customers = pd.read_csv(customer_features_path)
    rfm = pd.read_csv(rfm_path)

    # Keep only the frequency information needed from the RFM report.
    frequency = rfm[["customer_id", "frequency"]].copy()

    if customers["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs in customer features.")

    if frequency["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs in the RFM report.")

    df = customers.merge(
        frequency,
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    if len(df) != len(customers):
        raise ValueError("Customer count changed during the frequency merge.")

    if df["frequency"].isna().any():
        raise ValueError("Some customers do not have a frequency value.")

    # A tiny floating-point residual is effectively zero.
    # Do not overwrite the original customer feature file.
    near_zero = df["total_transaction_value"].abs() < 1e-9
    near_zero_count = int(near_zero.sum())

    print(f"\nCustomers available: {len(df):,}")
    print(f"Net monetary values normalized as zero for audit: {near_zero_count}")

    # Use features that describe customer purchase behavior.
    raw_features = df[FEATURE_COLUMNS].copy()

    if raw_features.isna().any().any():
        raise ValueError("Missing values found in clustering features.")

    if (raw_features < 0).any().any():
        raise ValueError(
            "Negative values found in selected clustering features. "
            "Investigate before applying log1p."
        )

    # Log1p safely handles zeros and reduces right skew.
    transformed = pd.DataFrame(index=df.index)

    transformed["recency_log"] = np.log1p(
        raw_features["recency_days"]
    )
    transformed["frequency_log"] = np.log1p(
        raw_features["frequency"]
    )
    transformed["positive_value_log"] = np.log1p(
        raw_features["positive_transaction_value"]
    )
    transformed["distinct_products_log"] = np.log1p(
        raw_features["distinct_products"]
    )

    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(transformed)

    scaled = pd.DataFrame(
        scaled_values,
        columns=[
            f"{column}_scaled"
            for column in transformed.columns
        ],
        index=df.index,
    )

    # Preserve customer IDs and original business metrics for interpretation.
    output = pd.concat(
        [
            df[
                [
                    "customer_id",
                    "recency_days",
                    "frequency",
                    "positive_transaction_value",
                    "distinct_products",
                ]
            ],
            transformed,
            scaled,
        ],
        axis=1,
    )

    if output.isna().any().any():
        raise ValueError("Missing values found in clustering output.")

    if not np.isfinite(scaled_values).all():
        raise ValueError("Non-finite values found after feature scaling.")

    output.to_csv(output_path, index=False)

    # Save an audit summary of the raw and transformed features.
    audit_rows = []

    for column in FEATURE_COLUMNS:
        audit_rows.append(
            {
                "feature": column,
                "raw_skewness": raw_features[column].skew(),
                "raw_minimum": raw_features[column].min(),
                "raw_median": raw_features[column].median(),
                "raw_mean": raw_features[column].mean(),
                "raw_maximum": raw_features[column].max(),
            }
        )

    for column in transformed.columns:
        audit_rows.append(
            {
                "feature": column,
                "raw_skewness": transformed[column].skew(),
                "raw_minimum": transformed[column].min(),
                "raw_median": transformed[column].median(),
                "raw_mean": transformed[column].mean(),
                "raw_maximum": transformed[column].max(),
            }
        )

    pd.DataFrame(audit_rows).to_csv(audit_path, index=False)

    print(f"\nPrepared customer rows: {len(output):,}")
    print(f"Raw behavioral features: {len(FEATURE_COLUMNS)}")
    print(f"Log-transformed features: {len(transformed.columns)}")
    print(f"Scaled features: {len(scaled.columns)}")

    print("\nScaled feature means (approximately zero):")
    print(scaled.mean().round(4).to_string())

    print("\nScaled feature standard deviations (approximately one):")
    print(scaled.std(ddof=0).round(4).to_string())

    print(f"\nClustering dataset saved to:\n{output_path}")
    print(f"\nFeature audit saved to:\n{audit_path}")

    print("\nFeature preparation completed successfully.")


if __name__ == "__main__":
    main()
