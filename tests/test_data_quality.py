import pandas as pd

from backend.data_quality import (
        get_missing_values, 
        get_duplicate_count,
        classify_transactions
    )


def test_get_missing_values():
    df = pd.DataFrame({
        "Product": ["Kalem", "Defter", "Silgi"],
        "Price": [10, None, 5],
        "Customer": [101, 102, None]
    })

    result = get_missing_values(df)

    assert result["Product"] == 0
    assert result["Price"] == 1
    assert result["Customer"] == 1
    
def test_get_duplicate_count():
    df = pd.DataFrame({
        "Product": ["Kalem", "Defter", "Kalem", "Silgi", "Defter"],
        "Price": [10, 20, 10, 5, 20]
    })

    result = get_duplicate_count(df)

    assert result == 2

def test_classify_transactions():
    df = pd.DataFrame({
        "Invoice": ["489434", "C489449", "489464", "489525"],
        "Quantity": [12, -12, -96, 1],
        "Price": [6.95, 2.95, 0.0, 0.55]
    })

    result = classify_transactions(df)

    assert result["TransactionType"].tolist() == [
        "Sale", "Cancellation", "Review", "Sale"
    ]

    assert result["IsCancelled"].tolist() == [
        False, True, False, False
    ]

    assert "TransactionType" not in df.columns
    assert "IsCancelled" not in df.columns