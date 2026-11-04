import pandas as pd
from pathlib import Path

from backend.analytics import (
    calculate_total_revenue,
    calculate_average_order_value,
    calculate_total_orders,
    get_top_selling_products
)
from backend.data_pipeline import (
    run_cleaning_pipeline,
    generate_cleaning_summary
)
from backend.report_generator import (
    save_quality_report,
    create_report_metadata
)
from backend.data_quality import (
    classify_transactions,
    get_missing_values,
    get_duplicate_count,
    generate_quality_summary
)

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
    raw_df = sample_df.copy()

    print(f"Satir sayisi: {sample_df.shape[0]}")
    print(f"Sutun sayisi: {sample_df.shape[1]}")

    print("\nEksik deger sayilari:")
    print(get_missing_values(sample_df))

    print("\nTekrarlanan satir sayisi:")
    print(get_duplicate_count(sample_df))

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

    sample_df = classify_transactions(sample_df)

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
    
    print("\n--- HAM VERI KALITESI OZETI ---")

    raw_quality_summary = generate_quality_summary(raw_df)

    for metric, value in raw_quality_summary.items():
        print(f"{metric}: {value}")

    print("\n--- ISLEM TURU SINIFLANDIRMASI ---")

    print(sample_df["TransactionType"].value_counts())

    print("\nIslem turune gore ornekler:")
    print(
        sample_df.groupby("TransactionType")[["Quantity", "Price"]]
        .agg(["count", "mean"])
    )

    print("\n--- OTOMATIK VERI KALITESI OZETI ---")

    quality_summary = generate_quality_summary(sample_df)

    for metric, value in quality_summary.items():
        print(f"{metric}: {value}")
    

    print("\n--- VERI TEMIZLEME PIPELINE ---")

    cleaned_df = run_cleaning_pipeline(raw_df)

    print(f"Ham veri satir sayisi: {len(raw_df)}")
    print(f"Temizlenmis veri satir sayisi: {len(cleaned_df)}")

    print("\nTemizlenmis veri islem turleri:")
    print(cleaned_df["TransactionType"].value_counts())

    print("\nTemizlenmis veride eksik musteri sayisi:")
    print(cleaned_df["Customer ID"].isna().sum())

    print("\nTemizlenmis veride tekrar eden satir sayisi:")
    print(cleaned_df.duplicated().sum())

    print("\n--- VERI TEMIZLEME OZET RAPORU ---")

    cleaning_summary = generate_cleaning_summary(
        raw_df,
        cleaned_df
    )

    for metric, value in cleaning_summary.items():
        print(f"{metric}: {value}")

    print("\n--- JSON RAPORU OLUSTURULUYOR ---")

    metadata = create_report_metadata(
        source=DATA_PATH.name,
        report_type="data_quality",
        sample_size=len(raw_df)
    )

    report_data = {
        "metadata": metadata,
        "quality_metrics": quality_summary,
        "cleaning_metrics": cleaning_summary
    }

    report_path = BASE_DIR / "reports" / "data_quality_report.json"

    saved_path = save_quality_report(
        report_data,
        report_path
    )

    print(f"Rapor basariyla kaydedildi: {saved_path}")


    print("\n--- SATIS ANALITIGI ---")

    total_revenue = calculate_total_revenue(cleaned_df)
    print(f"Toplam satis geliri: {total_revenue:,.2f}")
    
    average_order_value = calculate_average_order_value(cleaned_df)
    print(f"Ortalama siparis tutari (AOV): {average_order_value:,.2f}")
    
    total_orders = calculate_total_orders(cleaned_df)
    print(f"Toplam benzersiz siparis sayisi: {total_orders}")

    print("\n--- EN COK SATILAN 10 URUN ---")

    top_products = get_top_selling_products(
        cleaned_df,
        top_n=10
    )

    print(top_products.to_string(index=False))


if __name__ == "__main__":
    main()