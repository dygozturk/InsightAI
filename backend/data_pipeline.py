
import pandas as pd

from backend.data_quality import classify_transactions
from backend.data_cleaning import (
    remove_duplicates,
    handle_missing_customers,
    filter_transactions
)


def run_cleaning_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Veri temizleme adimlarini sirayla calistirir.
    Orijinal DataFrame'i degistirmez.
    """

    cleaned_df = df.copy()

    # 1. Islem turlerini siniflandir
    cleaned_df = classify_transactions(cleaned_df)

    # 2. Tekrarlanan kayitlari kaldir
    cleaned_df = remove_duplicates(cleaned_df)

    # 3. Eksik musteri numaralarini yonet
    cleaned_df = handle_missing_customers(cleaned_df)

    # 4. Sadece satis islemlerini al
    cleaned_df = filter_transactions(cleaned_df, "Sale")

    return cleaned_df


def generate_cleaning_summary(
    raw_df: pd.DataFrame,
    cleaned_df: pd.DataFrame
) -> dict:
    """
    Veri temizleme oncesi ve sonrasi
    karsilastirma raporu olusturur.
    """

    raw_rows = len(raw_df)
    cleaned_rows = len(cleaned_df)

    removed_rows = raw_rows - cleaned_rows

    retention_rate = (
        round((cleaned_rows / raw_rows) * 100, 2)
        if raw_rows > 0 else 0.0
    )

    summary = {
        "raw_rows": raw_rows,
        "cleaned_rows": cleaned_rows,
        "removed_rows": removed_rows,
        "retention_rate": retention_rate,
        "remaining_duplicates": int(
            cleaned_df.duplicated().sum()
        ),
        "remaining_missing_customers": int(
            cleaned_df["Customer ID"].isna().sum()
        )
    }

    return summary
