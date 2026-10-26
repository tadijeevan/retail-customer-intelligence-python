# Business Questions

## 1. Data Quality

- How many transaction records and columns are available?
- How many records have missing customer identifiers or product descriptions?
- How many exact duplicate rows exist?
- How many transactions contain cancellations, negative quantities, zero prices or negative prices?
- What date range does the dataset cover?

## 2. Sales and Product Performance

- How does transaction value change month over month?
- Which products contribute the highest net transaction values?
- Which products have high sales quantities?
- How do returns and cancellations affect product-level results?
- How should incomplete months be handled when comparing sales?

## 3. Customer Behaviour

- How many identifiable customers are present?
- How frequently do identifiable customers make repeat purchases?
- Which customers have purchased recently, frequently or at higher monetary values?
- Which customers fall into the rule-based RFM segments?
- How do customer activity and spending differ across the identified clusters?

## 4. Market Basket Analysis

- Which products appear together in the same analyzed invoice?
- Which product association rules meet the selected support and confidence thresholds?
- Which rules have comparatively high lift?
- How many analyzed invoices support each selected association?
- How can association rules inform product placement or cross-selling hypotheses?

## 5. Sales Forecasting

- How accurately can monthly transaction values be forecast using simple baselines?
- How does a previous-month forecast compare with a three-month moving average?
- Which method produces lower MAE and RMSE on the chronological evaluation period?
- How does the limited historical period affect confidence in the results?

## 6. Scope and Limitations

These analyses describe patterns in the UCI Online Retail dataset. They do not establish causation or guarantee future business outcomes. Results depend on data preparation, filters, metric definitions and the limited historical period.
