import pandas as pd
import pytest

from src.data_cleaning import (
    standardize_column_names,
    prepare_transaction_data,
)


def test_standardize_column_names():
    df = pd.DataFrame(
        columns=["InvoiceNo", "Stock Code", " Invoice Date "]
    )

    result = standardize_column_names(df)

    assert result.columns.tolist() == [
        "invoiceno",
        "stock_code",
        "invoice_date",
    ]


def test_prepare_transaction_data():
    df = pd.DataFrame(
        {
            "InvoiceNo": ["536365", "C536379"],
            "StockCode": ["85123A", "71053"],
            "InvoiceDate": ["2010-12-01", "2010-12-02"],
            "Quantity": [6, -2],
            "UnitPrice": [2.55, 3.39],
            "CustomerID": [17850, None],
        }
    )

    result = prepare_transaction_data(df)

    # Invoice and product identifiers should remain strings.
    assert pd.api.types.is_string_dtype(result["invoiceno"])
    assert pd.api.types.is_string_dtype(result["stockcode"])

    # Invoice dates should be datetime values.
    assert pd.api.types.is_datetime64_any_dtype(result["invoicedate"])

    # Cancellation flags should be correct.
    assert result["is_cancellation"].tolist() == [False, True]

    # Line values should be calculated correctly.
    assert result["line_value"].tolist() == pytest.approx([15.30, -6.78])

    # Missing customer IDs should remain missing.
    assert pd.isna(result.loc[1, "customerid"])