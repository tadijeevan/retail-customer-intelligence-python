import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names by removing extra spaces
    and converting names to lowercase with underscores.

    Example:
        InvoiceNo -> invoiceno
        Invoice Date -> invoice_date
    """
    cleaned_df = df.copy()

    cleaned_df.columns = (
        cleaned_df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return cleaned_df
def prepare_transaction_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize transaction columns and prepare data types.

    This function does not remove rows or handle missing values.
    """
    cleaned_df = standardize_column_names(df)

    # Preserve invoice and product identifiers as strings
    cleaned_df["invoiceno"] = cleaned_df["invoiceno"].astype("string")
    cleaned_df["stockcode"] = cleaned_df["stockcode"].astype("string")

    # Convert invoice dates to datetime
    cleaned_df["invoicedate"] = pd.to_datetime(
        cleaned_df["invoicedate"],
        errors="coerce"
    )

    # Convert numeric columns safely
    cleaned_df["quantity"] = pd.to_numeric(
        cleaned_df["quantity"],
        errors="coerce"
    )

    cleaned_df["unitprice"] = pd.to_numeric(
        cleaned_df["unitprice"],
        errors="coerce"
    )

    cleaned_df["customerid"] = pd.to_numeric(
        cleaned_df["customerid"],
        errors="coerce"
    )

        # Identify cancellation-style invoices
    cleaned_df["is_cancellation"] = (
        cleaned_df["invoiceno"].str.startswith("C", na=False)
    )

    # Calculate transaction line value
    cleaned_df["line_value"] = (
        cleaned_df["quantity"] * cleaned_df["unitprice"]
    )
    return cleaned_df