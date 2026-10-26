# Model Evaluation

## 1. Forecasting Evaluation

### Objective

Compare simple forecasting methods for monthly transaction values using chronological one-month-ahead predictions.

### Evaluation Design

- Complete months used: December 2010 through November 2011.
- Evaluation period: April through November 2011.
- Evaluation observations: 8 months.
- Methods: previous-month baseline and three-month moving average.
- Incomplete December 2011 was excluded from the complete-month evaluation.

### Results

| Forecast Method | MAE | RMSE |
|---|---:|---:|
| Previous-month baseline | 155,334.49 | 211,930.04 |
| Three-month moving average | 189,970.27 | 254,361.09 |

### Interpretation

The previous-month baseline produced lower MAE and RMSE than the three-month moving average over the reported evaluation period. Lower MAE and RMSE indicate smaller prediction errors under these metrics.

The evaluation covers only eight months. The result should therefore be treated as preliminary rather than proof that the previous-month baseline will always perform better.

## 2. Customer Clustering Evaluation

### Evaluation Approach

Candidate cluster counts from K = 2 through K = 8 were evaluated using silhouette scores. The reported evaluation used a sample of up to 2,000 records with random_state 42.

### Results

- Selected cluster count: K = 2.
- Reported silhouette score: approximately 0.3930.
- Cluster 0: 2,590 customers.
- Cluster 1: 1,749 customers.

### Interpretation

The two clusters show differences in recency, purchase frequency, transaction value and product diversity. One group generally has lower recent activity and lower purchase frequency; the other has more recent and frequent purchasing and higher spending.

The silhouette score is a diagnostic of cluster separation, not proof that the groups are stable, actionable or commercially useful. The cluster profiles should be validated before business use.

## 3. Overall Limitations and Recommendations

### Forecasting Limitations

- The evaluation covers only eight months.
- The dataset contains a limited historical period.
- Performance may change with different periods, transaction patterns or business conditions.
- Additional forecasting methods and longer rolling evaluations could provide a stronger comparison.

### Clustering Limitations

- The silhouette score does not establish business usefulness.
- Results depend on feature preparation, scaling, sample selection and model settings.
- Cluster stability should be checked across different samples and configurations.
- Segment descriptions should be validated against business requirements before operational use.

### Recommendations

- Preserve chronological evaluation to reduce the risk of using future information in forecasting.
- Compare model performance against simple baselines before selecting a more complex model.
- Document evaluation periods, metrics, assumptions and limitations.
- Re-evaluate models when more historical data becomes available.
