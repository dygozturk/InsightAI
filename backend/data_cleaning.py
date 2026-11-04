import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Veri setindeki tamamen ayni satirlari kaldirir.

    Orijinal DataFrame'i degistirmez.
    Temizlenmis yeni bir DataFrame dondurur.
    """

    cleaned_df = df.drop_duplicates().copy()

    return cleaned_df

def handle_missing_customers(
    df: pd.DataFrame,
    drop_missing: bool = False
) -> pd.DataFrame:
    """
    Eksik musteri numaralarini yonetir.

    drop_missing=False:
        Eksik musteri numarali kayitlari korur.

    drop_missing=True:
        Eksik musteri numarali kayitlari kaldirir.
    """

    cleaned_df = df.copy()

    if drop_missing:
        cleaned_df = cleaned_df.dropna(
            subset=["Customer ID"]
        )

    return cleaned_df

def filter_transactions(
    df: pd.DataFrame,
    transaction_type: str = "Sale"
) -> pd.DataFrame:
    """
    Veri setini islem turune gore filtreler.

    Sale: Normal satislar
    Cancellation: Iptal islemleri
    Review: Incelenmesi gereken kayitlar
    """

    valid_types = ["Sale", "Cancellation", "Review"]

    if transaction_type not in valid_types:
        raise ValueError(
            f"Gecersiz islem turu: {transaction_type}"
        )

    if "TransactionType" not in df.columns:
        raise ValueError(
            "TransactionType sutunu bulunamadi."
        )

    filtered_df = df[
        df["TransactionType"] == transaction_type
    ].copy()

    return filtered_df