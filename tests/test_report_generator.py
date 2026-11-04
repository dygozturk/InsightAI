import json
from pathlib import Path
from datetime import datetime, timezone
from backend.report_generator import (
    save_quality_report,
    create_report_metadata
)


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

def test_create_report_metadata():
    metadata = create_report_metadata(
        source="online_retail_II.xlsx",
        report_type="data_quality",
        sample_size=1000
    )

    # Veri kaynagi dogru mu?
    assert metadata["source"] == "online_retail_II.xlsx"

    # Rapor turu dogru mu?
    assert metadata["report_type"] == "data_quality"

    # Orneklem buyuklugu dogru mu?
    assert metadata["sample_size"] == 1000

    # Tarih bilgisi ISO 8601 formatinda mi?
    generated_at = datetime.fromisoformat(
        metadata["generated_at"]
    )

    # Tarih saat dilimi bilgisi iceriyor mu?
    assert generated_at.tzinfo is not None

    # Saat dilimi UTC mi?
    assert generated_at.utcoffset().total_seconds() == 0

def test_report_structure(tmp_path):
    metadata = create_report_metadata(
        source="online_retail_II.xlsx",
        report_type="data_quality",
        sample_size=1000
    )

    quality_metrics = {
        "total_rows": 1000,
        "total_columns": 10,
        "missing_values": 7,
        "duplicate_rows": 28,
        "invalid_quantity": 46,
        "invalid_price": 4
    }

    report_data = {
        "metadata": metadata,
        "quality_metrics": quality_metrics
    }

    report_path = tmp_path / "test_report.json"

    save_quality_report(report_data, report_path)

    import json

    with open(report_path, "r", encoding="utf-8") as file:
        saved_report = json.load(file)

    assert "metadata" in saved_report
    assert "quality_metrics" in saved_report
    assert saved_report["metadata"]["sample_size"] == 1000
    assert saved_report["quality_metrics"]["missing_values"] == 7


def test_report_with_cleaning_metrics():

    report_data = {
        "metadata": {
            "source": "online_retail_II.xlsx",
            "report_type": "data_quality",
            "sample_size": 1000
        },
        "quality_metrics": {
            "total_rows": 1000,
            "missing_values": 7
        },
        "cleaning_metrics": {
            "raw_rows": 1000,
            "cleaned_rows": 926,
            "removed_rows": 74,
            "retention_rate": 92.6,
            "remaining_duplicates": 0,
            "remaining_missing_customers": 2
        }
    }

    assert "metadata" in report_data
    assert "quality_metrics" in report_data
    assert "cleaning_metrics" in report_data

    assert report_data["cleaning_metrics"]["raw_rows"] == 1000
    assert report_data["cleaning_metrics"]["cleaned_rows"] == 926
    assert report_data["cleaning_metrics"]["removed_rows"] == 74

    assert (
        report_data["cleaning_metrics"]["retention_rate"]
        == 92.6
    )


def test_saved_json_report_structure():

    base_dir = Path(__file__).resolve().parent.parent

    report_path = (
        base_dir / "reports" / "data_quality_report.json"
    )

    assert report_path.exists(), "JSON raporu bulunamadi."

    with report_path.open("r", encoding="utf-8") as file:
        report_data = json.load(file)

    assert "metadata" in report_data
    assert "quality_metrics" in report_data
    assert "cleaning_metrics" in report_data

    cleaning = report_data["cleaning_metrics"]

    assert cleaning["raw_rows"] == 1000
    assert cleaning["cleaned_rows"] == 926
    assert cleaning["removed_rows"] == 74

    assert cleaning["retention_rate"] == 92.6
    assert cleaning["remaining_duplicates"] == 0
    assert cleaning["remaining_missing_customers"] == 2
