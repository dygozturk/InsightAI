from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "raw" / "online_retail_II.xlsx"


def main():
    print("InsightAI - Veri Kesfi")
    print(f"Pandas surumu: {pd.__version__}")

    if not DATA_PATH.exists():
        print(f"HATA: Veri dosyasi bulunamadi: {DATA_PATH}")
        return

    print("Excel dosyasi bulundu!")

    excel_file = pd.ExcelFile(DATA_PATH)
    print("Excel calisma sayfalari:")
    for sheet in excel_file.sheet_names:
        print(f"- {sheet}")

    print("\n--- ILK 5 SATIR ---")
    df = pd.read_excel(
        excel_file,
        sheet_name="Year 2009-2010",
        nrows=5
    )
    print(df.to_string(index=False))

    print("\n--- SUTUN ISIMLERI ---")
    print(df.columns.tolist())

    print("\n--- VERI TIPLERI ---")
    print(df.dtypes)
    print("\n--- ILK 1000 SATIR: VERI KALITESI ---")
    sample_df = pd.read_excel(
        excel_file,
        sheet_name="Year 2009-2010",
        nrows=1000,
        dtype={
            "Invoice": str,
            "StockCode": str,
            "Customer ID": str
        }
    )

    print(f"Satir sayisi: {sample_df.shape[0]}")
    print(f"Sutun sayisi: {sample_df.shape[1]}")

    print("\nEksik deger sayilari:")
    print(sample_df.isnull().sum())

    print("\nTekrarlanan satir sayisi:")
    print(sample_df.duplicated().sum())

    print("\nNegatif veya sifir miktarli kayit sayisi:")
    print((sample_df["Quantity"] <= 0).sum())

    print("\nNegatif veya sifir fiyatli kayit sayisi:")
    print((sample_df["Price"] <= 0).sum())
    
    print("\n--- NEGATIF VEYA SIFIR MIKTARLI KAYITLAR ---")
    invalid_quantity = sample_df[sample_df["Quantity"] <= 0]
    print(invalid_quantity.head(10).to_string(index=False))

    print("\n--- NEGATIF VEYA SIFIR FIYATLI KAYITLAR ---")
    invalid_price = sample_df[sample_df["Price"] <= 0]
    print(invalid_price.head(10).to_string(index=False))

    print("\n--- MUSTERI NUMARASI EKSIK KAYITLAR ---")
    missing_customers = sample_df[sample_df["Customer ID"].isna()]
    print(missing_customers.head(10).to_string(index=False))
    
    print("\n--- IPTAL ISLEMI ANALIZI ---")

    sample_df["IsCancelled"] = (
        sample_df["Invoice"].str.startswith("C", na=False)
    )

    cancelled_count = sample_df["IsCancelled"].sum()
    negative_quantity_count = (sample_df["Quantity"] < 0).sum()

    print(f"Iptal olarak isaretlenen satir sayisi: {cancelled_count}")
    print(f"Negatif miktarli satir sayisi: {negative_quantity_count}")

    print("\nIptal olarak isaretlenen ilk 5 satir:")
    print(
        sample_df.loc[
            sample_df["IsCancelled"],
            ["Invoice", "Quantity", "Price", "IsCancelled"]
        ].head(5).to_string(index=False)
    )

    print("\nC ile baslamayan negatif miktarli satir sayisi:")
    print(
        ((sample_df["Quantity"] < 0) & ~sample_df["IsCancelled"]).sum()
    )
    

    print("\n--- ISLEM TURU SINIFLANDIRMASI ---")

    conditions = [
        sample_df["IsCancelled"],
        (sample_df["Quantity"] <= 0) | (sample_df["Price"] <= 0)
    ]

    choices = ["Cancellation", "Review"]

    sample_df["TransactionType"] = np.select(
        conditions,
        choices,
        default="Sale"
    )

    print(sample_df["TransactionType"].value_counts())

    print("\nIslem turune gore ornekler:")
    print(
        sample_df.groupby("TransactionType")[["Quantity", "Price"]]
        .agg(["count", "mean"])
    )


if __name__ == "__main__":
    main()