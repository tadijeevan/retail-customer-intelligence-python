# Product Analysis Findings

## 1. Overview

This analysis examines product-level transaction values and quantities
in the UCI Online Retail dataset.

The prepared dataset contains 541,909 transaction rows. The analysis
preserves transaction records, including negative quantities and
cancellation-style invoices, so that positive and negative transaction
activity can be examined separately.

The purpose is to understand product performance while avoiding
misleading rankings based only on positive transaction values.

## 2. Methodology

The analysis groups transactions by stock code and calculates:

- Positive quantity: Sum of quantities greater than zero.
- Negative quantity: Sum of quantities less than zero.
- Net quantity: Sum of all quantities.
- Positive transaction value: Sum of positive line values.
- Negative transaction value: Sum of negative line values.
- Net transaction line value: Sum of all line values.
- Transaction rows: Number of transaction rows for each stock code.
- Cancellation rows: Number of rows flagged as cancellation invoices.

Line value is calculated as:

Quantity multiplied by UnitPrice.

Net transaction line value is an analytical measure. It must not
automatically be interpreted as recognized revenue or profit.

## 3. Merchandise Analysis

The current analysis excludes the specifically identified postage codes
DOT and POST and the manual adjustment code M from the merchandise
candidate summary.

All other stock codes remain merchandise candidates pending further
classification checks.

The following products ranked highest by net transaction line value
in the current analysis:

| Product | Net Transaction Line Value |
|---|---:|
| REGENCY CAKESTAND 3 TIER | £164,762.19 |
| WHITE HANGING HEART T-LIGHT HOLDER | £99,846.98 |
| PARTY BUNTING | £98,302.98 |
| JUMBO BAG RED RETROSPOT | £92,356.03 |
| RABBIT NIGHT LIGHT | £66,756.59 |

These results include negative transaction values rather than ranking
products only by their positive transaction lines.

The SMALL POPCORN HOLDER had the highest net quantity in the current
analysis, at 56,450 units.

## 4. Postage and Manual Adjustments

The following stock codes are initially classified separately:

| Category | Stock Code | Description |
|---|---|---|
| Postage | DOT | DOTCOM POSTAGE |
| Postage | POST | POSTAGE |
| Manual adjustment | M | Manual |

Their current net transaction line values are:

| Stock Code | Net Transaction Line Value |
|---|---:|
| DOT | £206,245.48 |
| POST | £66,230.64 |
| M | -£68,671.64 |

These are preliminary classifications based on the entries investigated
so far. Additional unusual stock codes may require further review.

## 5. Returns, Cancellations, and Reversals

Negative transaction values can materially change product rankings.

For example, stock code 23843, PAPER CRAFT, LITTLE BIRDIE, has a
positive transaction value of £168,469.60 and an equal negative
transaction value of -£168,469.60 in the matching transaction pair
investigated. Its net transaction line value for those two rows is zero.

Stock code 23166, MEDIUM CERAMIC TOP STORAGE JAR, also has substantial
negative transaction activity. Its previously investigated totals were:

- Positive transaction value: £81,700.92
- Negative transaction value: -£77,479.64
- Net transaction line value: £4,221.28
- Net quantity: 3,539

These examples show why positive transaction value alone can be
misleading.

Negative quantities and cancellation-style invoice numbers are not
assumed to have identical meanings. Their business interpretation
requires further investigation where relevant.

## 6. Data-Quality Considerations

The analysis follows these principles:

1. Preserve the original raw dataset.
2. Do not automatically remove duplicate-looking rows.
3. Retain negative quantities and cancellation records for analysis.
4. Define filters according to the business question.
5. Separate identified postage and manual adjustment codes from
   merchandise candidates.
6. Validate calculations against transaction-level records.
7. Document assumptions and limitations.

The classification of remaining stock codes is not yet complete.

## 7. Limitations

- Transaction line value is not necessarily recognized revenue or profit.
- The dataset contains duplicate-looking rows that require contextual
  investigation before any exclusions are considered.
- The business meaning of every negative transaction is not established.
- The merchandise category includes stock codes that have not all been
  independently validated as ordinary merchandise.
- The dataset covers December 2010 through December 9, 2011, so
  December 2011 represents only part of a month.
- Product rankings depend on the transaction definitions and filters
  used in the analysis.

## 8. Output Files

The current analysis produces:

- `reports/product_sales_analysis.csv`
- `reports/non_merchandise_analysis.csv`

The scripts used to generate these reports are stored in `src/`.

## 9. Next Steps

- Investigate additional unusual stock codes.
- Validate product-level calculations and classifications.
- Continue with customer-level analysis using identifiable customers.
- Build RFM features and interpretable customer segments.
- Document analytical assumptions and findings as the project develops.
