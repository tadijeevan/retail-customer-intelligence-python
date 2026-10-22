# Data Quality Findings

## 1. Overview

The original Online Retail dataset contains 541,909 transaction rows
and eight columns. This investigation evaluates missing values,
duplicate records, cancellations, quantities, prices, and invoice dates.

The original Excel dataset remains unchanged. Findings are documented
before deciding which records, if any, should be excluded from specific
analyses.

## 2. Key Findings

| Check | Rows | Percentage of Dataset |
|---|---:|---:|
| Total transaction rows | 541,909 | 100.00% |
| Exact duplicate rows | 5,268 | 0.97% |
| Missing customer IDs | 135,080 | 24.93% |
| Missing descriptions | 1,454 | 0.27% |
| Cancellation-style invoice rows | 9,288 | 1.71% |
| Negative quantity rows | 10,624 | 1.96% |
| Zero quantity rows | 0 | 0.00% |
| Zero unit-price rows | 2,515 | 0.46% |
| Negative unit-price rows | 2 | Approximately 0.00% |
| Missing invoice dates | 0 | 0.00% |
| Missing or unparseable invoice dates | 0 | 0.00% |

Percentages are calculated relative to the total number of transaction rows.
These categories can overlap, so their counts must not be added together
to estimate the total number of problematic records.

## 3. Business Impact

### Missing Customer IDs

Approximately 24.93% of transaction rows have no CustomerID.

Impact:
- These transactions cannot be assigned to a known customer.
- Customer-level analysis and RFM segmentation require identifiable customers.
- Excluding these records from customer-level analysis may reduce the
  transaction value represented in that analysis.

Decision:
Retain the original records. Exclude rows without CustomerID only from
analyses that require customer identification.

### Exact Duplicate Rows

The dataset contains 5,268 exact duplicate rows.

Impact:
- Duplicate records may inflate sales, quantities, and transaction counts.
- Some repeated product lines may be legitimate, so duplicates require
  investigation before removal.

Decision:
Do not automatically remove duplicates. Investigate them and document
the rules used for any analysis-specific exclusions.

### Cancellation-Style Invoices and Negative Quantities

There are 9,288 cancellation-style invoice rows and 10,624 rows with
negative quantities.

Impact:
- These records may represent returns, cancellations, or other adjustments.
- Including them without a defined rule may affect revenue and quantity
  calculations.

Decision:
Preserve these records in the original dataset. Define separate rules
for gross sales, returns, and net sales.

### Zero and Negative Unit Prices

The dataset contains 2,515 rows with zero unit prices and two rows with
negative unit prices.

Impact:
- Zero-price records may represent samples, adjustments, or other
  non-standard transactions.
- Negative prices require investigation before calculating sales value.

Decision:
Investigate these records before deciding how they should be treated
in each analysis. Do not assume every zero-price transaction is invalid.

### Missing Descriptions

There are 1,454 rows without a product description.

Impact:
- These records may be unsuitable for some product-level reporting.
- Other available transaction fields may still be useful.

Decision:
Retain the records and exclude missing descriptions only where product
description is required.

### Invoice Dates

No missing or unparseable invoice dates were identified.

Impact:
- The available invoice dates can support time-based analysis, subject
  to validation of the date range and reporting periods.

Decision:
Continue using invoice dates for time-based analysis.

## 4. Data Preparation Principles

1. Preserve the original raw dataset.
2. Standardize column names and data types.
3. Investigate anomalies before changing or removing records.
4. Keep customer-level and transaction-level analysis requirements separate.
5. Document filters and exclusions explicitly.
6. Validate the output after each preparation step.

## 5. Next Steps

- Define analysis-specific transaction filters.
- Prepare a consistent transaction dataset.
- Calculate sales value using Quantity multiplied by UnitPrice.
- Perform exploratory data analysis.
- Analyze sales by time, product, and country.
- Build customer-level metrics and RFM segments using identifiable customers.

## 6. Report Location

The consolidated CSV report is saved at:

`reports/data_quality_report.csv`

The original dataset is stored at:

`data/raw/Online Retail.xlsx`

The raw Excel file has not been modified.
