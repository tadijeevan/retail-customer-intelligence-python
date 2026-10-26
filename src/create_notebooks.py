from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = ROOT / "notebooks"

NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)


def markdown(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text):
    return nbf.v4.new_code_cell(text.strip())


def create_notebook(filename, title, description, cells):
    notebook = nbf.v4.new_notebook()
    notebook["cells"] = [
        markdown(f"# {title}\n\n{description}"),
        *cells,
    ]
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
    }

    output_path = NOTEBOOK_DIR / filename
    nbf.write(notebook, output_path)
    print(f"Created: {output_path.relative_to(ROOT)}")


# Shared project setup.
setup = code("""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path.cwd()
if not (ROOT / "reports").exists():
    ROOT = Path.cwd().parent

REPORTS = ROOT / "reports"
PROCESSED = ROOT / "data" / "processed"
FIGURES = REPORTS / "figures"

print("Project root:", ROOT)
print("Reports directory exists:", REPORTS.exists())
print("Processed data directory exists:", PROCESSED.exists())
""")


# 1. Data understanding.
notebook1 = [
    markdown("## 1. Project objectives\n\nUnderstand the UCI Online Retail transactions and establish data quality considerations before analysis."),
    setup,
    markdown("## 2. Dataset dimensions and schema"),
    code("""
data_path = PROCESSED / "online_retail_prepared.csv"
df = pd.read_csv(data_path)

print("Rows:", len(df))
print("Columns:", len(df.columns))
display(df.head())
display(df.dtypes.to_frame("data_type"))
"""),
    markdown("## 3. Missing values and duplicates"),
    code("""
quality = pd.DataFrame({
    "missing_count": df.isna().sum(),
    "missing_percent": (df.isna().mean() * 100).round(2),
})
display(quality.sort_values("missing_count", ascending=False))
print("Exact duplicate rows:", int(df.duplicated().sum()))
"""),
    markdown("## 4. Transaction anomalies\n\nCancellations, negative quantities, zero prices, and negative prices require business-aware interpretation. Do not automatically delete these rows."),
    code("""
df["invoiceno"] = df["invoiceno"].astype("string")
df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")

checks = {
    "Cancellation invoice rows": int(df["invoiceno"].str.startswith("C", na=False).sum()),
    "Negative quantity rows": int((df["quantity"] < 0).sum()),
    "Zero unit-price rows": int((df["unitprice"] == 0).sum()),
    "Negative unit-price rows": int((df["unitprice"] < 0).sum()),
    "Missing customer IDs": int(df["customerid"].isna().sum()),
    "Invalid invoice dates": int(df["invoicedate"].isna().sum()),
}
display(pd.Series(checks, name="count").to_frame())
"""),
    markdown("## 5. Data quality decisions\n\n- Retain the original dataset unchanged.\n- Preserve transaction rows in the prepared dataset.\n- Exclude unidentified customers only from analyses requiring customer identity.\n- Apply cancellation and product filters explicitly for each analytical task.\n- Treat net line value as an analytical measure, not necessarily recognized revenue or profit."),
]


# 2. Sales EDA.
notebook2 = [
    markdown("## 1. Business questions\n\nExplore monthly sales patterns, leading products, and country-level transaction distribution."),
    setup,
    markdown("## 2. Monthly sales trend"),
    code("""
monthly = pd.read_csv(REPORTS / "monthly_sales.csv")
display(monthly)

monthly["month"] = pd.to_datetime(monthly["month"])
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly["month"], monthly["sales_value"], marker="o")
ax.set_title("Monthly Transaction Line Value")
ax.set_xlabel("Month")
ax.set_ylabel("Line value (£)")
ax.grid(alpha=0.3)
fig.autofmt_xdate()
plt.show()
"""),
    markdown("## 3. Monthly growth"),
    code("""
display(monthly[["month", "sales_value", "mom_growth_percent"]])

print(
    "Caution: December 2011 covers only the first nine days "
    "of the month and must not be compared with full months "
    "as if it were complete."
)
"""),
    markdown("## 4. Product performance"),
    code("""
products = pd.read_csv(REPORTS / "product_sales_analysis.csv")
display(products.head(10))
"""),
    markdown("## 5. Data quality and interpretation\n\nSome stock codes may represent postage, adjustments, or other non-merchandise entries. Interpret product rankings using the documented classification rules."),
    code("""
non_merchandise_path = REPORTS / "non_merchandise_analysis.csv"
if non_merchandise_path.exists():
    display(pd.read_csv(non_merchandise_path))
"""),
]


# 3. Customer RFM.
notebook3 = [
    markdown("## 1. RFM framework\n\nRecency measures days since the last purchase; frequency measures distinct purchase invoices; monetary value measures net transaction line value."),
    setup,
    markdown("## 2. Customer-level RFM data"),
    code("""
rfm = pd.read_csv(REPORTS / "customer_rfm.csv")
scored = pd.read_csv(REPORTS / "customer_rfm_scored.csv")
segments = pd.read_csv(REPORTS / "customer_segments.csv")

print("Customers in RFM dataset:", len(rfm))
display(rfm.describe().T)
display(scored.head())
"""),
    markdown("## 3. Rule-based customer segments"),
    code("""
segment_summary = pd.read_csv(REPORTS / "customer_segment_summary.csv")
display(segment_summary)

segment_chart = FIGURES / "customer_count_by_segment.png"
if segment_chart.exists():
    from IPython.display import Image, display as show_image
    show_image(Image(filename=str(segment_chart)))
"""),
    markdown("## 4. K-Means clustering comparison"),
    code("""
evaluation_path = REPORTS / "clustering_model_evaluation.csv"
profiles_path = REPORTS / "customer_cluster_profiles.csv"

if evaluation_path.exists():
    display(pd.read_csv(evaluation_path))
if profiles_path.exists():
    display(pd.read_csv(profiles_path))
"""),
    markdown("## 5. Interpretation and limitations\n\nRFM segments are rule-based, while K-Means groups customers according to scaled behavioral features. Cluster labels are arbitrary. Inactivity is not confirmed churn, and the short observation window limits lifecycle conclusions."),
]


# 4. Market basket.
notebook4 = [
    markdown("## 1. Objective\n\nIdentify products that frequently occur together in the same invoice."),
    setup,
    markdown("## 2. Transaction preparation"),
    code("""
basket_path = PROCESSED / "market_basket_transactions.csv"
basket = pd.read_csv(basket_path, dtype={"invoiceno": "string", "stockcode": "string"})

print("Prepared rows:", len(basket))
print("Unique invoices:", basket["invoiceno"].nunique())
print("Unique products:", basket["stockcode"].nunique())
display(basket.head())
"""),
    markdown("## 3. Frequent itemsets"),
    code("""
itemsets = pd.read_csv(REPORTS / "frequent_itemsets.csv")
display(itemsets.head(10))
"""),
    markdown("## 4. Association rules"),
    code("""
rules_path = REPORTS / "market_basket_rules_enhanced.csv"
rules = pd.read_csv(rules_path)
display(rules.head(10))
"""),
    markdown("## 5. Interpreting rule metrics\n\n- Support: fraction of invoices containing the combined itemset.\n- Confidence: fraction of antecedent invoices that also contain the consequent.\n- Lift: observed co-occurrence relative to the consequent's baseline frequency.\n\nAssociation does not establish causation. Low-support rules should be interpreted cautiously."),
    code("""
metric_columns = [
    c for c in ["support", "confidence", "lift", "supporting_invoice_count"]
    if c in rules.columns
]
display(rules[metric_columns].describe().T)
"""),
]


# 5. Forecasting and validation.
notebook5 = [
    markdown("## 1. Forecasting objective\n\nCompare a previous-month baseline with a three-month moving average using chronological one-step-ahead evaluation."),
    setup,
    markdown("## 2. Monthly sales history"),
    code("""
monthly = pd.read_csv(REPORTS / "monthly_sales.csv")
monthly["month"] = pd.to_datetime(monthly["month"])
display(monthly)

print(
    "The December 2011 observation is incomplete and is excluded "
    "from the forecasting evaluation."
)
"""),
    markdown("## 3. Forecast predictions and metrics"),
    code("""
predictions = pd.read_csv(REPORTS / "forecast_predictions.csv")
metrics = pd.read_csv(REPORTS / "forecast_model_evaluation.csv")

display(predictions)
display(metrics)
"""),
    markdown("## 4. Forecast visualization"),
    code("""
chart = FIGURES / "forecast_evaluation.png"
if chart.exists():
    from IPython.display import Image, display as show_image
    show_image(Image(filename=str(chart)))
"""),
    markdown("## 5. Validation and limitations\n\nPredictions use only data available before each target month. The evaluation has only eight test months, so the results are uncertain. The previous-month baseline performed better on this sample, but this does not guarantee better future performance. Annual seasonality cannot be established reliably from this short history."),
    code("""
assert not predictions["month"].astype(str).str.endswith("-12").any()
assert predictions["month"].is_unique
assert predictions["actual_sales"].notna().all()
assert metrics["mae"].notna().all()
assert metrics["rmse"].notna().all()

print("Forecast validation checks passed.")
"""),
]


def main():
    notebooks = [
        ("01_data_understanding.ipynb", "01 — Data Understanding",
         "Dataset overview, schema, data quality, and preparation decisions.", notebook1),
        ("02_sales_eda.ipynb", "02 — Sales Exploratory Data Analysis",
         "Sales trends, product performance, and interpretation.", notebook2),
        ("03_customer_rfm.ipynb", "03 — Customer RFM and Segmentation",
         "Customer features, RFM scores, segments, and clustering.", notebook3),
        ("04_market_basket.ipynb", "04 — Market Basket Analysis",
         "Invoice-product preparation, frequent itemsets, and association rules.", notebook4),
        ("05_forecasting_and_validation.ipynb", "05 — Forecasting and Validation",
         "Chronological forecasting evaluation and validation checks.", notebook5),
    ]

    for filename, title, description, cells in notebooks:
        create_notebook(filename, title, description, cells)

    print(f"\nCreated {len(notebooks)} notebooks.")


if __name__ == "__main__":
    main()
