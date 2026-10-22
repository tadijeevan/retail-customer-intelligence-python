from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "online_retail_prepared.csv"
)

PRODUCT_OUTPUT_PATH = (
    PROJECT_ROOT / "reports" / "product_sales_analysis.csv"
)

NON_MERCHANDISE_OUTPUT_PATH = (
    PROJECT_ROOT / "reports" / "non_merchandise_analysis.csv"
)

# Initial classifications based on our investigation.
POSTAGE_CODES = {"DOT", "POST"}
ADJUSTMENT_CODES = {"M"}


def classify_stock_code(stockcode):
    """Classify identified postage and adjustment codes."""

    if pd.isna(stockcode):
        return "Unknown"

    stockcode = str(stockcode).strip().upper()

    if stockcode in POSTAGE_CODES:
        return "Postage"

    if stockcode in ADJUSTMENT_CODES:
        return "Manual adjustment"

    return "Merchandise candidate"


def main():
    """Analyze merchandise candidates and non-merchandise entries."""

    print("=" * 70)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("PRODUCT SALES AND NON-MERCHANDISE ANALYSIS")
    print("=" * 70)

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print(f"\nLoaded {len(df):,} transaction rows.")

    # Normalize stock codes for consistent classification.
    df["stockcode"] = df["stockcode"].astype("string").str.strip().str.upper()

    # Identify the initial categories.
    df["entry_category"] = df["stockcode"].apply(classify_stock_code)

    # Summarize all transaction activity without deleting returns
    # or cancellation records.
    def summarize_transactions(data):
        return (
            data.groupby("stockcode", dropna=False)
            .agg(
                description=("description", "first"),
                positive_quantity=(
                    "quantity",
                    lambda values: values[values > 0].sum(),
                ),
                negative_quantity=(
                    "quantity",
                    lambda values: values[values < 0].sum(),
                ),
                net_quantity=("quantity", "sum"),
                positive_value=(
                    "line_value",
                    lambda values: values[values > 0].sum(),
                ),
                negative_value=(
                    "line_value",
                    lambda values: values[values < 0].sum(),
                ),
                net_transaction_line_value=("line_value", "sum"),
                transaction_rows=("invoiceno", "size"),
                cancellation_rows=("is_cancellation", "sum"),
            )
            .reset_index()
        )

    # Merchandise candidates: excludes the specifically identified
    # postage and manual adjustment codes, but retains all other rows.
    merchandise_df = df[
        df["entry_category"] == "Merchandise candidate"
    ].copy()

    product_summary = summarize_transactions(merchandise_df)

    # Rank products by net transaction line value.
    top_by_net_value = product_summary.sort_values(
        "net_transaction_line_value",
        ascending=False,
    ).head(10)

    print("\nTop 10 merchandise candidates by net transaction line value:")

    print(
        top_by_net_value[
            [
                "stockcode",
                "description",
                "positive_value",
                "negative_value",
                "net_transaction_line_value",
                "net_quantity",
                "transaction_rows",
                "cancellation_rows",
            ]
        ].to_string(
            index=False,
            formatters={
                "positive_value": lambda value: f"£{value:,.2f}",
                "negative_value": lambda value: f"£{value:,.2f}",
                "net_transaction_line_value": lambda value: f"£{value:,.2f}",
            },
        )
    )

    # Rank products by net quantity.
    top_by_quantity = product_summary.sort_values(
        "net_quantity",
        ascending=False,
    ).head(10)

    print("\nTop 10 merchandise candidates by net quantity:")

    print(
        top_by_quantity[
            [
                "stockcode",
                "description",
                "positive_quantity",
                "negative_quantity",
                "net_quantity",
                "transaction_rows",
            ]
        ].to_string(index=False)
    )

    # Analyze postage and manual adjustment entries separately.
    non_merchandise_df = df[
        df["entry_category"].isin(["Postage", "Manual adjustment"])
    ].copy()

    non_merchandise_summary = (
        non_merchandise_df.groupby(
            ["entry_category", "stockcode"],
            dropna=False,
        )
        .agg(
            description=("description", "first"),
            positive_value=(
                "line_value",
                lambda values: values[values > 0].sum(),
            ),
            negative_value=(
                "line_value",
                lambda values: values[values < 0].sum(),
            ),
            net_transaction_line_value=("line_value", "sum"),
            positive_quantity=(
                "quantity",
                lambda values: values[values > 0].sum(),
            ),
            negative_quantity=(
                "quantity",
                lambda values: values[values < 0].sum(),
            ),
            net_quantity=("quantity", "sum"),
            transaction_rows=("invoiceno", "size"),
            cancellation_rows=("is_cancellation", "sum"),
        )
        .reset_index()
    )

    # Save both reports.
    PRODUCT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    product_summary.to_csv(PRODUCT_OUTPUT_PATH, index=False)
    non_merchandise_summary.to_csv(
        NON_MERCHANDISE_OUTPUT_PATH,
        index=False,
    )

    print("\nNon-merchandise summary:")
    print(
        non_merchandise_summary[
            [
                "entry_category",
                "stockcode",
                "description",
                "positive_value",
                "negative_value",
                "net_transaction_line_value",
                "transaction_rows",
            ]
        ].to_string(
            index=False,
            formatters={
                "positive_value": lambda value: f"£{value:,.2f}",
                "negative_value": lambda value: f"£{value:,.2f}",
                "net_transaction_line_value": lambda value: f"£{value:,.2f}",
            },
        )
    )

    print(f"\nMerchandise report saved to: {PRODUCT_OUTPUT_PATH}")
    print(
        "Non-merchandise report saved to: "
        f"{NON_MERCHANDISE_OUTPUT_PATH}"
    )

    print(
        "\nNote: Net transaction line value is an analytical measure, "
        "not necessarily recognized revenue or profit."
    )
    print(
        "Classification is preliminary. Other unusual stock codes "
        "may require further investigation."
    )
    print("\nProduct analysis completed successfully.")


if __name__ == "__main__":
    main()