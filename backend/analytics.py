import pandas as pd


def calculate_total_revenue(df: pd.DataFrame) -> float:
    """
    Temizlenmis satis verilerinden toplam
    satis gelirini hesaplar.

    Revenue = Quantity * Price

    Orijinal DataFrame degistirilmez.
    """

    required_columns = ["Quantity", "Price"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Gerekli sutun bulunamadi: {column}"
            )

    total_revenue = (
        df["Quantity"] * df["Price"]
    ).sum()

    return float(total_revenue)


def calculate_average_order_value(df: pd.DataFrame) -> float:
    """
    Benzersiz siparis basina ortalama satis tutarini hesaplar.
    """

    required_columns = ["Invoice", "Quantity", "Price"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Eksik sutun: {column}")

    if df.empty:
        return 0.0

    total_revenue = calculate_total_revenue(df)

    total_orders = df["Invoice"].nunique()

    if total_orders == 0:
        return 0.0

    return float(total_revenue / total_orders)


def calculate_total_orders(df: pd.DataFrame) -> int:
    """
    Veri setindeki benzersiz siparis sayisini hesaplar.
    """

    if "Invoice" not in df.columns:
        raise ValueError("Invoice sutunu bulunamadi.")

    return int(df["Invoice"].nunique())


def get_top_selling_products(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Toplam satilan miktara gore en cok
    satilan urunleri listeler.
    """

    required_columns = ["StockCode", "Description", "Quantity"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Eksik sutun: {column}")

    if top_n <= 0:
        raise ValueError("top_n pozitif bir sayi olmalidir.")

    top_products = (
        df.groupby(["StockCode", "Description"], dropna=False)["Quantity"]
        .sum()
        .reset_index()
        .sort_values(by="Quantity", ascending=False)
        .head(top_n)
    )

    return top_products


def get_top_revenue_products(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Urunleri toplam satis gelirine gore siralar.

    Quantity * Price = Revenue

    En yuksek gelir getiren ilk top_n urunu dondurur.
    """

    required_columns = [
        "StockCode",
        "Description",
        "Quantity",
        "Price"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Eksik sutun: {column}"
            )

    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n <= 0:
        raise ValueError(
            "top_n pozitif bir tam sayi olmalidir."
        )

    revenue_df = df.copy()

    revenue_df["Revenue"] = (
        revenue_df["Quantity"] * revenue_df["Price"]
    )

    top_products = (
        revenue_df.groupby(
            ["StockCode", "Description"],
            as_index=False
        )["Revenue"]
        .sum()
        .sort_values(
            by="Revenue",
            ascending=False
        )
        .head(top_n)
        .reset_index(drop=True)
    )

    return top_products
