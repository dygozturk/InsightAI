
import pandas as pd

from backend.data_pipeline import (
    run_cleaning_pipeline,
    generate_cleaning_summary
)


def test_run_cleaning_pipeline():

    df = pd.DataFrame({
        "Invoice": ["1001", "1001", "C1002", "1003"],
        "Quantity": [2, 2, -1, 3],
        "Price": [10.0, 10.0, 5.0, 0.0],
        "Customer ID": ["123", "123", "456", None]
    })

    cleaned_df = run_cleaning_pipeline(df)

    assert len(cleaned_df) == 1

    assert (
        cleaned_df["TransactionType"] == "Sale"
    ).all()

    assert len(df) == 4


def test_pipeline_preserves_missing_customers():

    df = pd.DataFrame({
        "Invoice": ["1001", "1002", "C1003"],
        "Quantity": [2, 5, -1],
        "Price": [10.0, 15.0, 5.0],
        "Customer ID": ["123", None, "456"]
    })

    cleaned_df = run_cleaning_pipeline(df)

    # Iki gecerli satis kaydi kalmali
    assert len(cleaned_df) == 2

    # Eksik musteri numarasi korunmali
    assert cleaned_df["Customer ID"].isna().sum() == 1

    # Iptal kayitlari bulunmamali
    assert (
        cleaned_df["TransactionType"] == "Sale"
    ).all()


def test_generate_cleaning_summary():

    raw_df = pd.DataFrame({
        "Customer ID": ["101", "102", None, "103"],
        "Quantity": [2, 3, 4, 5],
        "Price": [10.0, 20.0, 30.0, 40.0]
    })

    cleaned_df = raw_df.iloc[:2].copy()

    summary = generate_cleaning_summary(
        raw_df,
        cleaned_df
    )

    assert summary["raw_rows"] == 4
    assert summary["cleaned_rows"] == 2
    assert summary["removed_rows"] == 2
    assert summary["retention_rate"] == 50.0
    assert summary["remaining_duplicates"] == 0
    assert summary["remaining_missing_customers"] == 0
