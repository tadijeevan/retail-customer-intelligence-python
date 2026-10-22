from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent

    input_file = (
        project_root
        / "data"
        / "processed"
        / "online_retail_prepared.csv"
    )

    output_file = (
        project_root
        / "data"
        / "processed"
        / "market_basket_transactions.csv"
    )

    df = pd.read_csv(
        input_file,
        dtype={
            "invoiceno": "string",
            "stockcode": "string",
        },
    )

    original_rows = len(df)

    # Standardize codes and remove surrounding whitespace.
    df["invoiceno"] = df["invoiceno"].str.strip()
    df["stockcode"] = df["stockcode"].str.strip().str.upper()

    # Ensure the required numeric columns are numeric.
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unitprice"] = pd.to_numeric(df["unitprice"], errors="coerce")

    # Exclude cancellation invoices.
    df = df[~df["invoiceno"].str.startswith("C", na=False)].copy()
    rows_after_cancellation_filter = len(df)

    # Keep positive purchase quantities and prices for the initial analysis.
    df = df[
        (df["quantity"] > 0)
        & (df["unitprice"] > 0)
    ].copy()
    rows_after_purchase_filter = len(df)

    # Require invoice and product identifiers.
    df = df[
        df["invoiceno"].notna()
        & df["invoiceno"].ne("")
        & df["stockcode"].notna()
        & df["stockcode"].ne("")
    ].copy()

    # Preliminary exclusion of non-merchandise codes identified earlier.
    excluded_codes = {"DOT", "POST", "M"}
    df = df[~df["stockcode"].isin(excluded_codes)].copy()

    # Keep one occurrence of each product within each invoice.
    # Quantity is not used as the number of basket items.
    df = df.drop_duplicates(
        subset=["invoiceno", "stockcode"]
    ).copy()

    # Save the cleaned invoice-product rows.
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    print("=" * 70)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("MARKET BASKET DATA PREPARATION")
    print("=" * 70)

    print(f"\nOriginal transaction rows: {original_rows:,}")
    print(
        "Rows after excluding cancellation invoices: "
        f"{rows_after_cancellation_filter:,}"
    )
    print(
        "Rows after positive quantity and price filters: "
        f"{rows_after_purchase_filter:,}"
    )
    print(f"Rows in prepared basket data: {len(df):,}")
    print(f"Unique invoices: {df['invoiceno'].nunique():,}")
    print(f"Unique product codes: {df['stockcode'].nunique():,}")
    print(
        "Unique invoice-product combinations: "
        f"{df[['invoiceno', 'stockcode']].drop_duplicates().shape[0]:,}"
    )

    print("\nSample invoice-product rows:")
    print(
        df[["invoiceno", "stockcode", "description", "quantity"]]
        .head(10)
        .to_string(index=False)
    )

    print(f"\nPrepared basket transactions saved to:\n{output_file}")
    print("\nMarket basket data preparation completed.")


if __name__ == "__main__":
    main()
