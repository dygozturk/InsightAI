from pathlib import Path
import json


def save_quality_report(summary, output_path):
    """
    Veri kalitesi ozetini JSON dosyasina kaydeder.
    """

    output_path = Path(output_path)

    # Gerekirse hedef klasoru olustur
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Raporu JSON formatinda kaydet
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False
        )

    return output_path