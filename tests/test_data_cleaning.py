import pandas as pd
import pytest

from backend.data_cleaning import (
    remove_duplicates,
    handle_missing_customers,
    filter_transactions
)


def test_remove_duplicates():
    # Ornek veri seti
    df = pd.DataFrame({
        "Invoice": ["1001", "1001", "1002", "1003"],
        "Quantity": [5, 5, 10, 3],
        "Price": [2.5, 2.5, 4.0, 1.5]
    })

    # Temizleme fonksiyonunu calistir
    cleaned_df = remove_duplicates(df)

    # Tekrarlanan satir kaldirilmali
    assert len(cleaned_df) == 3

    # Orijinal veri korunmali
    assert len(df) == 4

    # Temizlenmis veride tekrar olmamali
    assert cleaned_df.duplicated().sum() == 0
    
def test_handle_missing_customers():
    # Ornek musteri verileri
    df = pd.DataFrame({
        "Invoice": ["1001", "1002", "1003", "1004"],
        "Customer ID": ["12345", None, "67890", None],
        "Quantity": [5, 3, 10, 2]
    })

    # Eksik kayitlari koruma
    kept_df = handle_missing_customers(
        df,
        drop_missing=False
    )

    assert len(kept_df) == 4
    assert kept_df["Customer ID"].isna().sum() == 2

    # Eksik kayitlari kaldirma
    cleaned_df = handle_missing_customers(
        df,
        drop_missing=True
    )

    assert len(cleaned_df) == 2
    assert cleaned_df["Customer ID"].isna().sum() == 0

    # Orijinal veri degismemeli
    assert len(df) == 4
    assert df["Customer ID"].isna().sum() == 2

def test_filter_transactions():
    df = pd.DataFrame({
        "Invoice": ["1001", "C1002", "1003", "1004"],
        "TransactionType": [
            "Sale",
            "Cancellation",
            "Sale",
            "Review"
        ],
        "Quantity": [5, -2, 10, -3]
    })

    sales_df = filter_transactions(df, "Sale")
    cancellations_df = filter_transactions(
        df, "Cancellation"
    )
    review_df = filter_transactions(df, "Review")

    assert len(sales_df) == 2
    assert len(cancellations_df) == 1
    assert len(review_df) == 1

    assert (sales_df["TransactionType"] == "Sale").all()

    # Orijinal veri korunmali
    assert len(df) == 4


def test_filter_transactions_invalid_type():
    df = pd.DataFrame({
        "TransactionType": ["Sale", "Review"]
    })

    with pytest.raises(ValueError):
        filter_transactions(df, "Unknown")


def test_filter_transactions_missing_column():
    df = pd.DataFrame({
        "Invoice": ["1001", "1002"]
    })

    with pytest.raises(ValueError):
        filter_transactions(df, "Sale")