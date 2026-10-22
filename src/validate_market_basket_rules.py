from pathlib import Path

import pandas as pd


def main():
    project_root = Path(__file__).resolve().parent.parent

    transactions_file = (
        project_root
        / "data"
        / "processed"
        / "market_basket_transactions.csv"
    )

    rules_file = (
        project_root
        / "reports"
        / "market_basket_rules_enhanced.csv"
    )

    transactions = pd.read_csv(
        transactions_file,
        dtype={
            "invoiceno": "string",
            "stockcode": "string",
        },
        low_memory=False,
    )

    rules = pd.read_csv(rules_file)

    # Normalize product codes for consistent comparisons.
    transactions["stockcode"] = (
        transactions["stockcode"]
        .str.strip()
        .str.upper()
    )

    # Identify the first rule for validation.
    target_rule = rules.iloc[0]

    antecedents = [
        code.strip()
        for code in target_rule["antecedents"].split(" | ")
    ]

    consequents = [
        code.strip()
        for code in target_rule["consequents"].split(" | ")
    ]

    antecedent_set = set(antecedents)
    consequent_set = set(consequents)
    combined_set = antecedent_set | consequent_set

    # Build invoice-level product sets.
    invoice_products = (
        transactions.groupby("invoiceno")["stockcode"]
        .agg(set)
    )

    total_invoices = len(invoice_products)

    antecedent_count = invoice_products.apply(
        lambda products: antecedent_set.issubset(products)
    ).sum()

    consequent_count = invoice_products.apply(
        lambda products: consequent_set.issubset(products)
    ).sum()

    combined_count = invoice_products.apply(
        lambda products: combined_set.issubset(products)
    ).sum()

    support = combined_count / total_invoices

    confidence = (
        combined_count / antecedent_count
        if antecedent_count
        else 0
    )

    consequent_support = (
        consequent_count / total_invoices
    )

    lift = (
        confidence / consequent_support
        if consequent_support
        else 0
    )

    print("=" * 65)
    print("MARKET BASKET RULE VALIDATION")
    print("=" * 65)

    print(f"\nTotal invoices: {total_invoices:,}")
    print(f"Antecedent products: {antecedents}")
    print(f"Consequent products: {consequents}")

    print("\nExact invoice counts:")
    print(f"Antecedent count: {antecedent_count:,}")
    print(f"Consequent count: {consequent_count:,}")
    print(f"Combined count: {combined_count:,}")

    print("\nRecalculated metrics:")
    print(f"Support: {support:.6f}")
    print(f"Confidence: {confidence:.6f}")
    print(f"Lift: {lift:.6f}")

    print("\nMetrics recorded in enhanced report:")
    print(f"Support: {target_rule['support']:.6f}")
    print(f"Confidence: {target_rule['confidence']:.6f}")
    print(f"Lift: {target_rule['lift']:.6f}")

    print("\nValidation completed.")


if __name__ == "__main__":
    main()