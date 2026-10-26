# Data Dictionary

## 1. Transaction Data

The project uses the UCI Online Retail dataset. Each row represents a product line on an invoice.

| Column | Description |
|---|---|
| InvoiceNo | Invoice identifier. Values beginning with C commonly indicate cancellations. |
| StockCode | Identifier assigned to a product or item. |
| Description | Product description. May contain missing values. |
| Quantity | Number of units. Negative values may represent returns or adjustments. |
| InvoiceDate | Date and time of the invoice. |
| UnitPrice | Unit price recorded for the item. |
| CustomerID | Customer identifier. May be missing. |
| Country | Customer country recorded in the dataset. |
| line_value | Derived transaction-line value, generally Quantity multiplied by UnitPrice. |

**Important:** `line_value` is an analytical transaction value, not necessarily recognized revenue or profit.

## 2. Customer RFM Analysis

RFM stands for Recency, Frequency and Monetary Value.

| Metric | Description |
|---|---|
| CustomerID | Identifier for an identifiable customer. |
| Recency | Days since the most recent qualifying purchase. Lower values indicate more recent activity. |
| Frequency | Number of distinct qualifying invoices associated with the customer. |
| Monetary | Net transaction value attributed to the customer under the project calculation rules. |
| RFM scores | Scores derived from recency, frequency and monetary metrics. |
| Customer segment | Rule-based grouping assigned using the project segmentation logic. |

## 3. Customer Clustering

| Field | Description |
|---|---|
| Cluster | Identifier assigned by the clustering model. |
| Recency and frequency | Customer activity measures used to describe clusters. |
| Monetary metrics | Transaction-value measures used in cluster profiling. |
| Product diversity | Number of distinct products purchased, where included in the cluster profile. |

Cluster identifiers are numerical labels, not rankings. Interpretations are provisional and should be validated before business use.

## 4. Monthly Sales and Forecasting

| Field | Description |
|---|---|
| Month | Calendar month associated with aggregated transactions. |
| Monthly sales | Sum of transaction-line values included in the monthly aggregation. |
| Actual sales | Observed monthly value used for forecast evaluation. |
| Predicted sales | Value estimated by a forecasting method. |
| Model | Forecasting approach used to generate a prediction. |
| MAE | Mean Absolute Error: average absolute difference between actual and predicted values. |
| RMSE | Root Mean Squared Error: square root of the average squared prediction error. |

The source data ends on 9 December 2011, making December 2011 incomplete. Account for this limitation when comparing monthly sales.

## 5. Market Basket Analysis

| Metric | Description |
|---|---|
| Antecedents | Product or products on the left-hand side of an association rule. |
| Consequents | Product or products on the right-hand side of an association rule. |
| Support | Proportion of analyzed transactions containing the required item combination. |
| Confidence | Proportion of transactions containing the antecedent that also contain the consequent. |
| Lift | Ratio of observed rule confidence to the consequent support. Lift above 1 indicates a positive association. |

Association rules describe purchasing patterns; they do not establish causation.

## 6. Data Interpretation Notes

- Customer-level analysis depends on records with usable customer identifiers.
- Returns, cancellations, zero prices and unusual transaction values require careful interpretation.
- Metric definitions depend on the relevant pipeline transformations and analysis filters.
- Consult the methodology and findings documents for processing rules, analytical results and limitations.
