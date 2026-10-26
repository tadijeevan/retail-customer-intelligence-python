# Methodology

## 1. Project Overview

This project analyzes the UCI Online Retail dataset using Python. The workflow covers data preparation, data quality assessment, exploratory data analysis, customer segmentation, market basket analysis and monthly sales forecasting.

## 2. Data Preparation

- Load the source transaction data.
- Standardize column names and prepare transaction fields for analysis.
- Derive transaction-line values using quantity and unit price.
- Apply the transformations implemented in the project pipeline.
- Save prepared data and analytical outputs for reuse.

Data preparation does not necessarily mean every unusual transaction has been removed. Interpret results using the documented filters and business rules.

## 3. Data Quality Assessment

Assess missing values, duplicate rows, cancellation invoices, negative quantities, zero prices, negative prices and date coverage. Treat these as distinct quality indicators because they can have different business meanings.

## 4. Exploratory Data Analysis

Aggregate transaction values over time and by product. Review monthly patterns and product performance. Treat December 2011 as a partial month because the source ends on 9 December 2011.

## 5. Customer RFM Segmentation

Calculate customer recency, frequency and monetary value using the project calculation rules. Derive RFM scores and assign rule-based customer segments. Customers without usable customer identifiers cannot be included in customer-level analysis.

## 6. Customer Clustering

Apply the clustering workflow to prepared customer features. Compare candidate cluster counts using silhouette scores and describe the resulting groups using customer activity and spending metrics.

Cluster labels are descriptive identifiers rather than business rankings. Results depend on feature preparation, scaling, model settings and the analyzed sample.

## 7. Market Basket Analysis

Analyze products purchased together within invoices. Use the project association-rule workflow and its configured support and confidence thresholds. Interpret support, confidence and lift together, and treat the resulting associations as hypotheses rather than causal findings.

## 8. Sales Forecasting

Aggregate transaction values by month and exclude the incomplete final month from the complete-month evaluation. Compare a previous-month baseline with a three-month moving-average forecast using chronological one-month-ahead predictions.

Evaluate predictions using mean absolute error (MAE) and root mean squared error (RMSE). The limited number of complete months restricts the strength of conclusions about future performance.

## 9. Reproducibility

Use the project dependency file, follow the setup guide, execute the pipeline and run the automated tests. Review the notebooks and generated reports to understand the results.

## 10. Limitations

- The dataset covers a limited historical period.
- Missing customer identifiers limit customer-level coverage.
- Returns, cancellations and unusual prices require careful interpretation.
- Forecast performance on a short evaluation period may not generalize.
- Customer segments and product associations require further validation before operational use.
