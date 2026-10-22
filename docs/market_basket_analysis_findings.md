# Market Basket Analysis — Findings and Business Insights

## 1. Business Objective

The objective of this analysis is to identify products that are frequently purchased together. These associations can help a retailer explore product bundling, cross-selling, and related-product recommendations.

## 2. Dataset Overview

The analysis uses the UCI Online Retail dataset, which contains historical retail transactions.

| Metric                                   |  Result |
| ---------------------------------------- | ------: |
| Original transaction rows                | 541,909 |
| Invoices included in basket analysis     |  19,792 |
| Unique product codes in prepared baskets |   3,809 |
| Frequent itemsets identified             |   2,000 |
| Association rules generated              |   1,676 |

## 3. Data Preparation

The basket preparation process applied the following rules:

* Excluded cancellation invoices.
* Retained transactions with positive quantities and positive unit prices.
* Excluded records without invoice or product identifiers.
* Excluded the preliminary non-merchandise codes `DOT`, `POST`, and `M`.
* Removed duplicate invoice-product combinations so that each product is represented only once per invoice.

These decisions were made specifically for market basket analysis. They do not mean that the original dataset was modified or that the same filters should be applied to every other analysis.

## 4. Methodology

The Apriori algorithm was used to identify frequently purchased product combinations and generate association rules.

The analysis used these thresholds:

* **Minimum support:** 0.01 (1%)
* **Minimum confidence:** 0.30 (30%)
* **Maximum itemset length:** 3

### Key Metrics

**Support:** The proportion of analysed invoices containing the specified item combination.

**Confidence:** The proportion of invoices containing the antecedent that also contain the consequent.

**Lift:** The ratio of the observed confidence to the consequent's support. It measures how much more frequently the antecedent and consequent occur together than would be expected if they were independent.

A lift greater than 1 indicates a positive association. Higher lift indicates a stronger association relative to the products' individual frequencies, but it does not prove causation or business profitability.

## 5. Key Findings

The highest-lift rules prominently featured these products:

* Stock code `22916`: HERB MARKER THYME
* Stock code `22917`: HERB MARKER ROSEMARY
* Stock code `22918`: HERB MARKER PARSLEY
* Stock code `22920`: HERB MARKER BASIL

### Example Association

**Rule:**

HERB MARKER THYME → HERB MARKER ROSEMARY + HERB MARKER PARSLEY

| Metric                                        | Validated result |
| --------------------------------------------- | ---------------: |
| Total invoices analysed                       |           19,792 |
| Invoices containing Thyme                     |              237 |
| Invoices containing both Rosemary and Parsley |              215 |
| Invoices containing all three products        |              203 |
| Support                                       |          1.0257% |
| Confidence                                    |         85.6540% |
| Lift                                          |          78.8495 |

### Interpretation

The rule indicates that, among the analysed invoices containing HERB MARKER THYME, approximately 85.65% also contained both HERB MARKER ROSEMARY and HERB MARKER PARSLEY.

The combination appeared in 203 out of 19,792 invoices, representing approximately 1.03% of all analysed invoices.

The recalculated support, confidence, and lift matched the values in the enhanced association-rules report. The supporting invoice count was verified directly against invoice-level transaction data.

The high lift indicates a strong association relative to the individual occurrence rates of the antecedent and consequent. However, the relatively low support means that this particular combination appeared in only a small proportion of all invoices.

## 6. Potential Business Applications

The identified associations suggest several opportunities for further investigation:

1. **Product bundling:** Test whether complementary herb markers could be offered together.
2. **Cross-selling:** Recommend related products when a customer views or purchases one of these items.
3. **Merchandising:** Evaluate whether related products should be displayed together.
4. **Recommendation systems:** Use validated associations as one input to product recommendation logic.

These are potential applications, not proven business outcomes. Their impact would need to be measured through appropriate experiments or business performance analysis.

## 7. Limitations

* The dataset covers a historical period from December 2010 to December 2011.
* The results describe historical purchasing patterns and may not reflect current customer behaviour.
* Association does not establish causation.
* The preliminary classification of non-merchandise codes may require further validation.
* The minimum support and confidence thresholds affect which itemsets and rules are discovered.
* A high lift does not necessarily imply high sales volume or profitability.
* The results depend on the invoice preparation and product deduplication rules used for this analysis.
* Returns, cancellations, and duplicate records were handled specifically for this analysis and may need different treatment for other business questions.
* The analysis identifies associations, not the reasons customers purchase products together.

## 8. Conclusion

The market basket analysis identified strong historical associations among several products, particularly the herb markers for Thyme, Rosemary, Parsley, and Basil.

The validated example rule showed that 203 invoices contained Thyme, Rosemary, and Parsley together. Its confidence was approximately 85.65%, and its lift was approximately 78.85.

These results demonstrate how transaction-level data can be transformed into product association insights using Python and the Apriori algorithm.

Potential next steps include investigating additional rules, evaluating the commercial relevance of the identified associations, testing product recommendations, and incorporating validated findings into the broader retail customer intelligence project.
