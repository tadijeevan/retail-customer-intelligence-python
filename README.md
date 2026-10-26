# Retail Customer Intelligence & Segmentation

A Python-based retail analytics project focused on sales performance, customer segmentation, purchasing behavior, market basket analysis, and sales forecasting.

## Project Overview

This project analyzes the UCI Online Retail dataset to transform transaction-level data into actionable business insights.

The analysis covers data preparation, exploratory data analysis (EDA), customer segmentation using Recency, Frequency, and Monetary (RFM) metrics, market basket analysis, and monthly sales forecasting.

The project demonstrates practical skills in Python, data analysis, statistical evaluation, data quality, and reproducible analytics workflows.

## Business Objectives

* Analyze sales trends and revenue patterns over time.
* Identify top-performing products and markets.
* Understand customer purchasing behavior.
* Calculate Recency, Frequency, and Monetary (RFM) metrics.
* Segment customers using clustering techniques.
* Explore product associations through market basket analysis.
* Evaluate forecasting approaches against a baseline model.
* Document data quality considerations and analytical limitations.

## Dataset

**Source:** UCI Machine Learning Repository — Online Retail

The dataset contains transactions from a UK-based online retailer covering December 2010 through December 2011.

* Dataset: https://archive.ics.uci.edu/dataset/352/online+retail
* Citation: Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository.
* DOI: https://doi.org/10.24432/C5BW33

The original dataset is not included in this repository. Download it separately and place the Excel file at `data/raw/Online Retail.xlsx` before running the data-preparation workflow.

## Technology Stack

| Category         | Technologies        |
| ---------------- | ------------------- |
| Programming      | Python              |
| Data analysis    | Pandas, NumPy       |
| Visualization    | Matplotlib, Seaborn |
| Machine learning | Scikit-learn, SciPy |
| Forecasting      | Statsmodels         |
| Notebooks        | Jupyter Notebook    |
| Testing          | Pytest              |
| Version control  | Git, GitHub         |

## Analytical Workflow

1. **Data preparation:** Load the source dataset, clean transaction data, and prepare an analysis-ready dataset.
2. **Exploratory analysis:** Examine transaction patterns, sales trends, product performance, and data quality.
3. **Customer analytics:** Calculate RFM metrics and investigate customer purchasing behavior.
4. **Customer segmentation:** Apply clustering techniques to identify groups with similar purchasing characteristics.
5. **Market basket analysis:** Explore product associations and frequent purchasing combinations.
6. **Sales forecasting:** Compare forecasting performance against a previous-month baseline.
7. **Validation and documentation:** Run automated tests and document methodology, findings, and model evaluation.

## Key Findings

The analysis produced the following headline results:

| Metric                                          |                      Result |
| ----------------------------------------------- | --------------------------: |
| Original transaction records                    |                     541,909 |
| Records with missing Customer IDs               |                      24.93% |
| Identifiable customers included in RFM analysis |                       4,339 |
| Total transaction line value                    | Approximately £9.75 million |

**Interpretation:** Missing Customer IDs are an important data quality limitation for customer-level analysis. Transaction-level sales analysis and customer-level segmentation therefore require different considerations.

These figures describe the analyzed dataset and are not estimates of future business performance.

## Sales Forecasting Evaluation

Two approaches were evaluated using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

| Forecasting approach       |        MAE |       RMSE |
| -------------------------- | ---------: | ---------: |
| Previous-month baseline    | 155,334.49 | 211,930.04 |
| Three-month moving average | 189,970.27 | 254,361.09 |

**Result:** The previous-month baseline performed better than the three-month moving average on both evaluation metrics. This demonstrates why a simple baseline should be established before adopting a more complex forecasting approach.

December 2011 is a partial month in the source dataset and was excluded from forecast evaluation.

## Project Notebooks

Explore the notebooks in sequence to follow the analysis:

1. [`01_data_understanding.ipynb`](notebooks/01_data_understanding.ipynb) — Dataset structure and initial data understanding.
2. [`02_sales_analysis.ipynb`](notebooks/02_sales_analysis.ipynb) — Sales trends and transaction analysis.
3. [`03_customer_rfm.ipynb`](notebooks/03_customer_rfm.ipynb) — Customer RFM analysis and segmentation.
4. [`04_market_basket.ipynb`](notebooks/04_market_basket.ipynb) — Market basket analysis and product associations.
5. [`05_forecasting.ipynb`](notebooks/05_forecasting.ipynb) — Forecasting approaches and evaluation.

## Repository Structure

```text
retail-customer-intelligence-python/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── notebooks/
├── reports/
│   └── figures/
├── src/
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Getting Started

### Prerequisites

* Python 3.13.6, the version used during development
* Git
* PowerShell on Windows, for the commands below

### 1. Clone the repository

```powershell
git clone https://github.com/tadijeevan/retail-customer-intelligence-python.git
cd retail-customer-intelligence-python
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks virtual environment activation, review your local execution-policy settings before making changes.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Prepare the dataset

1. Download the Online Retail dataset from the UCI link above.
2. Place the downloaded Excel file at `data/raw/Online Retail.xlsx`.
3. Run the preparation module from the repository root:

```powershell
python -m src.prepare_data
```

This creates the prepared transaction dataset under `data/processed/`.

### 5. Run the analytics pipeline

```powershell
python -m src.pipeline
```

### 6. Run automated tests

```powershell
python -m pytest -v
```

### 7. Explore the notebooks

```powershell
python -m pip install notebook ipykernel nbformat nbclient
python -m notebook
```

## Documentation

Additional documentation is available in the `docs/` directory, including setup instructions, data definitions, analytical methodology, findings, and model evaluation.

Generated reports and visualizations are available under `reports/` when the corresponding workflows have been run.

## Limitations and Future Improvements

* Missing Customer IDs limit customer-level analysis for a portion of transactions.
* The source dataset covers a limited historical period.
* Forecasting performance should be reassessed on additional time periods and with suitable time-series validation.
* Future work could evaluate richer forecasting models, additional customer features, and more robust out-of-sample validation.

## Reproducibility and Data Handling

* Keep the original dataset and generated customer-level files out of version control.
* Review generated outputs before sharing them publicly.
* Run project commands from the repository root.
* Results may vary with dependency versions, source data, and configuration changes.

## Author

**Jeevan Tadi**

GitHub: https://github.com/tadijeevan
