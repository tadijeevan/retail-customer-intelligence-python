# Setup Guide

## 1. Prerequisites

- Python 3.13.6 was used during project development.
- Git is required to clone the repository.
- PowerShell commands below assume a Windows environment.

## 2. Get the Project

Clone the repository:

    git clone https://github.com/tadijeevan/retail-customer-intelligence-python.git
    cd retail-customer-intelligence-python

## 3. Create and Activate a Virtual Environment

On Windows PowerShell, run:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

If PowerShell blocks activation, review your local execution-policy settings before making changes.

## 4. Install Dependencies

Activate the virtual environment, then install the project dependencies:

    python -m pip install --upgrade pip
    pip install -r requirements.txt

## 5. Prepare the Dataset

Download the UCI Online Retail dataset from its official source:

    https://archive.ics.uci.edu/dataset/352/online+retail

Place the downloaded source file in the location expected by the project data-preparation module. Check src/prepare_data.py to confirm the expected input path and file format before running the pipeline.

Do not commit the raw dataset or sensitive customer-level outputs to the public repository.

## 6. Run the Analytics Pipeline

From the repository root, execute:

    python -m src.pipeline

The pipeline runs the configured processing and analytics modules. Review the console output for errors and inspect the generated reports.

## 7. Run Automated Tests

Execute the test suite:

    python -m pytest -v

Tests should pass before changes are committed. Add tests when new transformations or analytical logic are introduced.

## 8. Explore the Notebooks

Install the notebook tools if they are not already installed:

    pip install notebook ipykernel nbformat nbclient

Start Jupyter Notebook:

    python -m notebook

Open the notebooks in the notebooks directory and execute their cells in order when appropriate.

## 9. Review Outputs

- Review generated CSV reports in the reports directory.
- Review visualizations in reports/figures.
- Consult data_dictionary.md for field definitions.
- Consult methodology.md, findings.md and model_evaluation.md for analytical methods, results and limitations.

## 10. Reproducibility and Safety

- Run commands from the repository root unless otherwise specified.
- Keep the local virtual environment and raw data out of version control.
- Inspect customer-level outputs before sharing or committing them.
- Results may vary with dependency versions, source data and configuration changes.
