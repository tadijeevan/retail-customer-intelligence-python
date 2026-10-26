# Project Findings

## 1. Dataset Overview

- Source: UCI Online Retail dataset.
- Original transaction rows: 541,909.
- Columns in the original dataset: 8.
- Unique invoices: approximately 25,900.
- Unique product codes: approximately 4,070.
- Identifiable customers: approximately 4,372 before customer-level purchase filters.
- Countries represented: 38.
- Source date range: 1 December 2010 to 9 December 2011.

## 2. Data Quality Findings

- Missing CustomerID values: 135,080, approximately 24.93% of source rows.
- Exact duplicate rows: 5,268.
- Cancellation invoice rows: 9,288.
- Rows with negative quantities: 10,624.
- Rows with zero UnitPrice: 2,515.
- Rows with negative UnitPrice: 2.
- Rows with missing Description: 1,454.
- Rows with zero Quantity: 0.
- No missing or invalid invoice dates were identified in the recorded quality assessment.

The prepared dataset retained 541,909 rows. These quality counts describe source records and should not be interpreted as counts of mutually exclusive problems.

## 3. Sales and Product Findings

- Total calculated transaction-line value: approximately £9,747,747.93.
- November 2011 had a recorded monthly value of approximately £1,461,756.25.
- December 2011 recorded approximately £433,668.01, but this is a partial month because the source ends on 9 December.
- High-value product codes included 22423, 85123A, 47566, 85099B and 23084.

Transaction-line value is an analytical measure, not a confirmed measure of recognized revenue or profit. Returns, cancellations and unusual prices affect interpretation.

## 4. Customer Purchase Behaviour

- Identifiable customers with at least one qualifying non-cancellation purchase: 4,339.
- Customers with two or more distinct regular invoices: 2,845.
- Repeat-customer percentage under this definition: approximately 65.57%.

## 5. RFM Analysis

- Analysis reference date: 10 December 2011.
- Customers included: 4,339.
- Mean recency: approximately 93.04 days; median recency: 51 days.
- Mean purchase frequency: approximately 4.27 invoices; median frequency: 2.
- Mean monetary value: approximately £1,915.30; median monetary value: £654.92.
- Nine customers had zero net monetary value and nine had negative net monetary value.

The RFM results depend on the transaction filters and monetary calculation used in the project. Negative monetary values require careful interpretation.

## 6. Rule-Based Customer Segments

| Segment | Customers | Share |
|---|---:|---:|
| Other Customers | 1,157 | 26.67% |
| Champions | 913 | 21.04% |
| Low-Activity Customers | 787 | 18.14% |
| Needs Attention | 717 | 16.52% |
| Loyal Customers | 379 | 8.73% |
| Recent Customers | 237 | 5.46% |
| High-Spending Customers | 149 | 3.43% |

These are rule-based segments. Interpret them according to the segmentation logic implemented in the project.

## 7. Market Basket Analysis

- Analyzed invoice-product records: 517,478.
- Analyzed invoices: 19,792.
- Product codes included: 3,809.
- Minimum support threshold: 1%.
- Minimum confidence threshold: 30%.
- Frequent itemsets generated: 2,000.
- Association rules generated: 1,676.

### Example Association Rule

- Antecedent: thyme.
- Consequents: rosemary and parsley.
- Support: approximately 1.03%.
- Confidence: approximately 85.65%.
- Lift: approximately 78.85.
- Combined invoices supporting the rule: 203.

This rule indicates a strong association within the analyzed transactions. It does not establish that purchasing thyme causes customers to purchase rosemary and parsley. Results depend on the invoice preparation and configured thresholds.

## 8. Customer Clustering

- Candidate cluster counts evaluated: K = 2 through K = 8.
- Highest silhouette score among the evaluated candidates: approximately 0.3930 at K = 2.
- Cluster 0: 2,590 customers, approximately 59.69% of the clustered customers.
- Cluster 1: 1,749 customers, approximately 40.31% of the clustered customers.

### Cluster Profiles

| Metric | Cluster 0 | Cluster 1 |
|---|---:|---:|
| Mean recency (days) | 135.13 | 30.71 |
| Median recency (days) | 96 | 18 |
| Mean purchase frequency | 1.64 | 8.17 |
| Median purchase frequency | 1 | 5 |
| Mean positive transaction value | £517.31 | £4,329.08 |
| Median positive transaction value | £352.18 | £1,981.92 |
| Mean distinct products | 25.44 | 115.29 |

Cluster 0 generally represents lower recent activity and lower purchasing frequency, while Cluster 1 represents more recent and frequent purchasing with higher spending. These are provisional interpretations based on the reported profiles.

The silhouette score is a diagnostic, not proof of business usefulness. The score was evaluated using a sample of up to 2,000 records with random_state 42. Cluster stability and business relevance require further validation.

## 9. Sales Forecasting and Model Evaluation

- Complete months available for the forecasting analysis: 12, from December 2010 through November 2011.
- Evaluation period: April through November 2011, covering 8 months.
- Forecast approaches compared: previous-month baseline and three-month moving average.

| Forecast Method | MAE | RMSE |
|---|---:|---:|
| Previous-month baseline | 155,334.49 | 211,930.04 |
| Three-month moving average | 189,970.27 | 254,361.09 |

The previous-month baseline achieved lower MAE and RMSE than the three-month moving average on this evaluation period.

The evaluation contains only eight months, so these results are preliminary and may not generalize to future periods. Forecast errors should be interpreted alongside the limited historical data and the transaction-value calculation.

## 10. Overall Conclusions

- The dataset contains useful information for transaction quality assessment, product analysis and customer behaviour analysis.
- RFM segmentation and clustering provide complementary ways to describe customer activity.
- Market basket rules identify product associations that may warrant further business investigation.
- The previous-month baseline outperformed the three-month moving average in the reported forecast evaluation.
- Data limitations, transaction adjustments and the short historical period should be considered before using these findings for business decisions.
