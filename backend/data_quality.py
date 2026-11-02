import pandas as pd


def get_missing_values(df: pd.DataFrame) -> pd.Series:
    """Veri setindeki sutunlarin eksik deger sayilarini hesaplar."""
    return df.isna().sum()

def get_duplicate_count(df: pd.DataFrame) -> int:
    """Veri setindeki tekrar eden satir sayisini hesaplar."""
    return int(df.duplicated().sum())