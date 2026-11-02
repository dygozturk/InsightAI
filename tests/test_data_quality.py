import pandas as pd

from backend.data_quality import get_missing_values, get_duplicate_count


def test_get_missing_values():
    df = pd.DataFrame({
        "Product": ["Kalem", "Defter", "Silgi"],
        "Price": [10, None, 5],
        "Customer": [101, 102, None]
    })

    result = get_missing_values(df)

    assert result["Product"] == 0
    assert result["Price"] == 1
    assert result["Customer"] == 1
    
def test_get_duplicate_count():
    df = pd.DataFrame({
        "Product": ["Kalem", "Defter", "Kalem", "Silgi", "Defter"],
        "Price": [10, 20, 10, 5, 20]
    })

    result = get_duplicate_count(df)

    assert result == 2
