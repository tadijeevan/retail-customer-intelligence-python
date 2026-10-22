from pathlib import Path

import pandas as pd


def describe_items(item_text, descriptions):
    codes = str(item_text).split(" | ")
    return " + ".join(
        f"{code} ({descriptions.get(code, 'Description unavailable')})"
        for code in codes
    )


def main():
    project_root = Path(__file__).resolve().parent.parent

    transactions_file = (
        project_root
        / "data"
        / "processed"
        / "market_basket_transactions.csv"
    )
    rules_file = project_root / "reports" / "market_basket_rules.csv"
    output_file = project_root / "reports" / "market_basket_rules_enhanced.csv"

    # Read invoice numbers as strings to avoid mixed-type warnings.
    transactions = pd.read_csv(
        transactions_file,
        dtype={"invoiceno": "string", "stockcode": "string"},
        low_memory=False,
    )

    rules = pd.read_csv(rules_file)

    # Build a consistent product-code-to-description lookup.
    product_lookup = (
        transactions.dropna(subset=["stockcode", "description"])
        .assign(
            stockcode=lambda frame: frame["stockcode"].str.strip().str.upper(),
            description=lambda frame: frame["description"].str.strip(),
        )
        .drop_duplicates(subset=["stockcode"])
    )

    descriptions = dict(
        zip(product_lookup["stockcode"], product_lookup["description"])
    )

    # Calculate the number of invoices represented by each rule's support.
    invoice_count = transactions["invoiceno"].nunique()

    rules["supporting_invoice_count"] = (
        rules["support"] * invoice_count
    ).round().astype(int)

    rules["antecedent_descriptions"] = rules["antecedents"].apply(
        lambda items: describe_items(items, descriptions)
    )

    rules["consequent_descriptions"] = rules["consequents"].apply(
        lambda items: describe_items(items, descriptions)
    )

    # Put the business-friendly fields first.
    output_columns = [
        "antecedents",
        "antecedent_descriptions",
        "consequents",
        "consequent_descriptions",
        "support",
        "supporting_invoice_count",
        "confidence",
        "lift",
        "leverage",
        "conviction",
    ]

    rules = rules[output_columns].sort_values(
        ["lift", "confidence", "support"],
        ascending=[False, False, False],
    )

    rules.to_csv(output_file, index=False)

    print("=" * 70)
    print("ENHANCED MARKET BASKET ANALYSIS REPORT")
    print("=" * 70)

    print(f"\nTotal invoices analysed: {invoice_count:,}")
    print(f"Association rules enhanced: {len(rules):,}")

    print("\nTop 10 rules by lift:")
    print(
        rules.head(10)[
            [
                "antecedent_descriptions",
                "consequent_descriptions",
                "support",
                "supporting_invoice_count",
                "confidence",
                "lift",
            ]
        ].to_string(
            index=False,
            formatters={
                "support": "{:.4f}".format,
                "confidence": "{:.4f}".format,
                "lift": "{:.3f}".format,
            },
        )
    )

    print(f"\nEnhanced report saved to:\n{output_file}")
    print("\nEnhanced report generation completed.")


if __name__ == "__main__":
    main()
