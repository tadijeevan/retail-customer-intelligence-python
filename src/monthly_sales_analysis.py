from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "online_retail_prepared.csv"
)


def main():
    """Analyze monthly retail sales value."""

    print("=" * 65)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("MONTHLY SALES ANALYSIS")
    print("=" * 65)

    # Step 1: Load the prepared dataset
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Prepared dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["invoicedate"],
    )

    print(f"\nDataset loaded: {len(df):,} rows")

    # Step 2: Create a monthly period column
    df["month"] = df["invoicedate"].dt.to_period("M")

    # Step 3: Calculate monthly sales value
    monthly_sales = (
        df.groupby("month")["line_value"]
        .sum()
        .reset_index()
    )

    monthly_sales["month"] = monthly_sales["month"].astype(str)

    monthly_sales = monthly_sales.rename(
        columns={
            "month": "Month",
            "line_value": "Sales_Value",
        }
    )

    # Step 4: Calculate month-over-month percentage change
    monthly_sales["MoM_Growth_Percent"] = (
        monthly_sales["Sales_Value"]
        .pct_change()
        .mul(100)
        .round(2)
    )

    # Step 5: Display results
    print("\nMonthly sales value and month-over-month growth:")

    print(
        monthly_sales.to_string(
            index=False,
            formatters={
                "Sales_Value": lambda value: f"£{value:,.2f}",
                "MoM_Growth_Percent": lambda value: (
                    "N/A" if pd.isna(value) else f"{value:.2f}%"
                ),
            },
        )
    )

    # Step 6: Identify the highest and lowest monthly totals
    highest_month = monthly_sales.loc[
        monthly_sales["Sales_Value"].idxmax()
    ]

    lowest_month = monthly_sales.loc[
        monthly_sales["Sales_Value"].idxmin()
    ]

    print("\nMonthly sales summary:")
    print(
        f"Highest monthly total: {highest_month['Month']} "
        f"(£{highest_month['Sales_Value']:,.2f})"
    )
    print(
        f"Lowest monthly total: {lowest_month['Month']} "
        f"(£{lowest_month['Sales_Value']:,.2f})"
    )

    # Step 7: Save the monthly summary
    output_path = (
        PROJECT_ROOT / "reports" / "monthly_sales_analysis.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    monthly_sales.to_csv(output_path, index=False)

    print(f"\nMonthly report saved to: {output_path}")
    print("\nMonthly sales analysis completed successfully.")


if __name__ == "__main__":
    main()
