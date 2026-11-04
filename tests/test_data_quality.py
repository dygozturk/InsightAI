import pandas as pd

from backend.data_quality import (
        get_missing_values, 
        get_duplicate_count,
        classify_transactions,
        generate_quality_summary
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
    
def test_generate_quality_summary():
    # Test icin kucuk bir veri seti olusturuyoruz.
    df = pd.DataFrame({
        "Quantity": [2, 2, -1, 0],
        "Price": [10.0, 10.0, 5.0, 0.0],
        "Description": ["Kalem", "Kalem", None, "Defter"]
    })

    # Fonksiyonu calistiriyoruz.
    summary = generate_quality_summary(df)

    # Bekledigimiz sonuclari kontrol ediyoruz.
    assert summary["total_rows"] == 4
    assert summary["total_columns"] == 3
    assert summary["missing_values"] == 1
    assert summary["duplicate_rows"] == 1
    assert summary["invalid_quantity"] == 2
    assert summary["invalid_price"] == 1

def test_raw_data_integrity():
    # Ornek ham veri
    raw_df = pd.DataFrame({
        "Invoice": ["489434", "C489449", "489435"],
        "Quantity": [12, -2, 5],
        "Price": [6.95, 2.50, 3.00]
    })

    # Ham verinin bagimsiz kopyasi
    sample_df = raw_df.copy()

    # Kopya uzerinde siniflandirma
    processed_df = classify_transactions(sample_df)

    # Ham veri degismemeli
    assert raw_df.shape == (3, 3)
    assert "TransactionType" not in raw_df.columns
    assert "IsCancelled" not in raw_df.columns

    # Islenmis veri yeni sutunlari icermeli
    assert processed_df.shape == (3, 5)
    assert "TransactionType" in processed_df.columns
    assert "IsCancelled" in processed_df.columns

    # Orijinal degerler korunmali
    assert raw_df["Quantity"].tolist() == [12, -2, 5]