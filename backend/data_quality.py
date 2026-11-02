import pandas as pd
import numpy as np


def get_missing_values(df: pd.DataFrame) -> pd.Series:
    """Veri setindeki sutunlarin eksik deger sayilarini hesaplar."""
    return df.isna().sum()

def get_duplicate_count(df: pd.DataFrame) -> int:
    """Veri setindeki tekrar eden satir sayisini hesaplar."""
    return int(df.duplicated().sum())

def classify_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Islemleri satis, iptal veya inceleme olarak siniflandirir."""

    result = df.copy()

    result["IsCancelled"] = (
        result["Invoice"].astype("string").str.startswith("C", na=False)
    ).astype(bool)

    conditions = [
        result["IsCancelled"],
        (result["Quantity"] <= 0) | (result["Price"] <= 0)
    ]

    choices = ["Cancellation", "Review"]

    result["TransactionType"] = np.select(
        conditions,
        choices,
        default="Sale"
    )

    return result