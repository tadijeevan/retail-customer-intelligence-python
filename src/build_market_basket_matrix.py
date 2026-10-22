from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent

    input_file = (
        project_root
        / "data"
        / "processed"
        / "market_basket_transactions.csv"
    )

    output_file = (
        project_root
        / "data"
        / "processed"
        / "market_basket_matrix.csv"
    )

    df = pd.read_csv(
        input_file,
        dtype={
            "invoiceno": "string",
            "stockcode": "string",
        },
    )

    # Each invoice-product combination should appear only once.
    df = df.drop_duplicates(subset=["invoiceno", "stockcode"])

    # Build a Boolean matrix: True means the product appears in the invoice.
    basket = pd.crosstab(
        df["invoiceno"],
        df["stockcode"],
    ).gt(0)

    # Store the matrix as integers (1 = present, 0 = absent).
    basket = basket.astype("int8")

    basket.to_csv(output_file, index=True, index_label="invoiceno")

    print("=" * 70)
    print("MARKET BASKET ANALYSIS")
    print("INVOICE-PRODUCT MATRIX")
    print("=" * 70)

    print(f"\nNumber of invoices: {basket.shape[0]:,}")
    print(f"Number of products: {basket.shape[1]:,}")
    print(f"Matrix dimensions: {basket.shape[0]:,} x {basket.shape[1]:,}")
    print(f"Total product presences: {int(basket.to_numpy().sum()):,}")

    print("\nFirst 5 invoices and first 10 product columns:")
    print(basket.iloc[:5, :10].to_string())

    print(f"\nMatrix saved to:\n{output_file}")
    print("\nInvoice-product matrix preparation completed.")


if __name__ == "__main__":
    main()
