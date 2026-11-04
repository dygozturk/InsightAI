import json

from backend.report_generator import save_quality_report


def test_save_quality_report(tmp_path):
    # Ornek veri kalitesi raporu
    summary = {
        "total_rows": 1000,
        "total_columns": 8,
        "missing_values": 7,
        "duplicate_rows": 28,
        "invalid_quantity": 46,
        "invalid_price": 4
    }

    # Gecici klasorde rapor yolu
    output_path = tmp_path / "reports" / "quality_report.json"

    # Fonksiyonu calistir
    result = save_quality_report(summary, output_path)

    # Dosya gercekten olusturuldu mu?
    assert output_path.exists()

    # Fonksiyon dogru dosya yolunu dondurdu mu?
    assert result == output_path

    # JSON dosyasini oku
    with open(output_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    # Kaydedilen veriler dogru mu?
    assert saved_data == summary