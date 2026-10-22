from pathlib import Path

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def main():
    project_root = Path(__file__).resolve().parent.parent

    input_file = (
        project_root
        / "data"
        / "processed"
        / "market_basket_transactions.csv"
    )
    itemsets_output = project_root / "reports" / "frequent_itemsets.csv"
    rules_output = project_root / "reports" / "market_basket_rules.csv"

    min_support = 0.01
    min_confidence = 0.30

    df = pd.read_csv(
        input_file,
        dtype={"invoiceno": "string", "stockcode": "string"},
    )

    # One presence per product per invoice.
    df = df.drop_duplicates(subset=["invoiceno", "stockcode"])

    # Create a Boolean invoice-product matrix.
    basket = pd.crosstab(df["invoiceno"], df["stockcode"]).gt(0)

    print("=" * 70)
    print("RETAIL CUSTOMER INTELLIGENCE PROJECT")
    print("MARKET BASKET ANALYSIS")
    print("=" * 70)
    print(f"\nInvoices: {basket.shape[0]:,}")
    print(f"Products: {basket.shape[1]:,}")
    print(f"Minimum support: {min_support:.0%}")
    print(f"Minimum confidence: {min_confidence:.0%}")
    print("\nFinding frequent itemsets with Apriori...")

    frequent_itemsets = apriori(
        basket,
        min_support=min_support,
        use_colnames=True,
        max_len=3,
        low_memory=True,
    )

    if frequent_itemsets.empty:
        raise ValueError(
            "No frequent itemsets found. Consider reviewing min_support."
        )

    frequent_itemsets["itemset_size"] = frequent_itemsets[
        "itemsets"
    ].apply(len)

    frequent_itemsets["items"] = frequent_itemsets["itemsets"].apply(
        lambda items: " | ".join(sorted(items))
    )

    itemsets_output.parent.mkdir(parents=True, exist_ok=True)

    frequent_itemsets[
        ["items", "itemset_size", "support"]
    ].sort_values(
        ["itemset_size", "support"],
        ascending=[True, False],
    ).to_csv(itemsets_output, index=False)

    print(f"Frequent itemsets found: {len(frequent_itemsets):,}")

    print("\nGenerating association rules...")

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence,
    )

    if rules.empty:
        print(
            "No association rules met the confidence threshold. "
            "The frequent itemsets were still saved."
        )
        print(f"\nFrequent itemsets saved to:\n{itemsets_output}")
        return

    rules["antecedents"] = rules["antecedents"].apply(
        lambda items: " | ".join(sorted(items))
    )
    rules["consequents"] = rules["consequents"].apply(
        lambda items: " | ".join(sorted(items))
    )

    rules = rules[
        [
            "antecedents",
            "consequents",
            "support",
            "confidence",
            "lift",
            "leverage",
            "conviction",
        ]
    ].sort_values(
        ["lift", "confidence", "support"],
        ascending=[False, False, False],
    )

    rules.to_csv(rules_output, index=False)

    print(f"Association rules found: {len(rules):,}")

    print("\nTop 10 association rules by lift:")
    print(
        rules.head(10).to_string(
            index=False,
            formatters={
                "support": "{:.4f}".format,
                "confidence": "{:.4f}".format,
                "lift": "{:.3f}".format,
                "leverage": "{:.5f}".format,
                "conviction": "{:.3f}".format,
            },
        )
    )

    print(f"\nFrequent itemsets saved to:\n{itemsets_output}")
    print(f"Association rules saved to:\n{rules_output}")
    print("\nMarket basket analysis completed.")


if __name__ == "__main__":
    main()
