import pandas as pd
import pytest

from backend.analytics import (
    calculate_total_revenue,
    calculate_average_order_value,
    calculate_total_orders,
    get_top_selling_products,
    get_top_revenue_products
)


def test_calculate_total_revenue():

    df = pd.DataFrame({
        "Quantity": [2, 3, 1],
        "Price": [10.0, 15.0, 30.0]
    })

    result = calculate_total_revenue(df)

    assert result == 95.0


def test_calculate_average_order_value():

    df = pd.DataFrame({
        "Invoice": ["1001", "1001", "1002"],
        "Quantity": [2, 1, 3],
        "Price": [10.0, 20.0, 15.0]
    })

    result = calculate_average_order_value(df)

    assert result == 42.5


def test_average_order_value_empty_dataframe():

    df = pd.DataFrame({
        "Invoice": [],
        "Quantity": [],
        "Price": []
    })

    result = calculate_average_order_value(df)

    assert result == 0.0


def test_average_order_value_missing_column():

    df = pd.DataFrame({
        "Invoice": ["1001"],
        "Quantity": [2]
    })

    with pytest.raises(ValueError):
        calculate_average_order_value(df)


def test_calculate_total_orders():

    df = pd.DataFrame({
        "Invoice": ["1001", "1001", "1002", "1003", "1003"]
    })

    result = calculate_total_orders(df)

    assert result == 3


def test_calculate_total_orders_missing_column():

    df = pd.DataFrame({
        "Quantity": [2, 3, 1]
    })

    import pytest

    with pytest.raises(ValueError):
        calculate_total_orders(df)


def test_get_top_selling_products():

    df = pd.DataFrame({
        "StockCode": ["A01", "B02", "A01", "C03", "B02"],
        "Description": ["Kalem", "Defter", "Kalem", "Silgi", "Defter"],
        "Quantity": [5, 3, 7, 2, 4]
    })

    result = get_top_selling_products(df, top_n=2)

    assert len(result) == 2

    assert result.iloc[0]["StockCode"] == "A01"
    assert result.iloc[0]["Quantity"] == 12

    assert result.iloc[1]["StockCode"] == "B02"
    assert result.iloc[1]["Quantity"] == 7


def test_get_top_selling_products_invalid_top_n():

    df = pd.DataFrame({
        "StockCode": ["A01", "B02"],
        "Description": ["Kalem", "Defter"],
        "Quantity": [5, 3]
    })

    import pytest

    with pytest.raises(ValueError):
        get_top_selling_products(df, top_n=0)


def test_get_top_selling_products_missing_column():

    df = pd.DataFrame({
        "StockCode": ["A01", "B02"],
        "Quantity": [5, 3]
    })

    import pytest

    with pytest.raises(ValueError):
        get_top_selling_products(df)


def test_get_top_selling_products_empty_dataframe():

    df = pd.DataFrame({
        "StockCode": [],
        "Description": [],
        "Quantity": []
    })

    result = get_top_selling_products(df, top_n=10)

    assert result.empty
    assert len(result) == 0


def test_get_top_selling_products_top_n_exceeds_products():

    df = pd.DataFrame({
        "StockCode": ["A01", "B02", "C03"],
        "Description": ["Kalem", "Defter", "Silgi"],
        "Quantity": [5, 10, 3]
    })

    result = get_top_selling_products(df, top_n=10)

    assert len(result) == 3
    assert result.iloc[0]["StockCode"] == "B02"
    assert result.iloc[0]["Quantity"] == 10


def test_get_top_selling_products_missing_description():

    df = pd.DataFrame({
        "StockCode": ["A01", "B02", "A01"],
        "Description": [None, "Defter", None],
        "Quantity": [5, 3, 7]
    })

    result = get_top_selling_products(df, top_n=10)

    assert len(result) == 2
    assert result.iloc[0]["StockCode"] == "A01"
    assert result.iloc[0]["Quantity"] == 12
    assert pd.isna(result.iloc[0]["Description"])


def test_get_top_selling_products_descending_order():

    df = pd.DataFrame({
        "StockCode": ["A01", "B02", "C03", "D04"],
        "Description": ["Kalem", "Defter", "Silgi", "Kitap"],
        "Quantity": [10, 50, 5, 25]
    })

    result = get_top_selling_products(df, top_n=4)

    quantities = result["Quantity"].tolist()

    assert quantities == [50, 25, 10, 5]


def test_get_top_revenue_products():

    df = pd.DataFrame({
        "StockCode": ["A01", "B02", "A01", "C03"],
        "Description": ["Kalem", "Defter", "Kalem", "Silgi"],
        "Quantity": [5, 2, 3, 10],
        "Price": [10.0, 50.0, 10.0, 5.0]
    })

    result = get_top_revenue_products(df, top_n=2)

    assert len(result) == 2

    assert result.iloc[0]["StockCode"] == "B02"
    assert result.iloc[0]["Revenue"] == 100.0

    assert result.iloc[1]["StockCode"] == "A01"
    assert result.iloc[1]["Revenue"] == 80.0


def test_get_top_revenue_products_missing_column():

    df = pd.DataFrame({
        "StockCode": ["A01", "B02"],
        "Description": ["Kalem", "Defter"],
        "Quantity": [5, 2]
    })

    with pytest.raises(ValueError, match="Eksik sutun: Price"):
        get_top_revenue_products(df)


@pytest.mark.parametrize(
    "invalid_top_n",
    [0, -1, 2.5, "5", None, True]
)
def test_get_top_revenue_products_invalid_top_n(invalid_top_n):

    df = pd.DataFrame({
        "StockCode": ["A01"],
        "Description": ["Kalem"],
        "Quantity": [5],
        "Price": [10.0]
    })

    with pytest.raises(ValueError, match="top_n pozitif bir tam sayi olmalidir"):
        get_top_revenue_products(df, top_n=invalid_top_n)


def test_get_top_revenue_products_empty_dataframe():

    df = pd.DataFrame(columns=[
        "StockCode",
        "Description",
        "Quantity",
        "Price"
    ])

    result = get_top_revenue_products(df)

    assert result.empty
    assert "Revenue" in result.columns
    assert len(result) == 0


def test_get_top_revenue_products_does_not_modify_original():

    df = pd.DataFrame({
        "StockCode": ["A01", "B02"],
        "Description": ["Kalem", "Defter"],
        "Quantity": [5, 2],
        "Price": [10.0, 50.0]
    })

    original_df = df.copy(deep=True)

    get_top_revenue_products(df)

    pd.testing.assert_frame_equal(df, original_df)

    assert "Revenue" not in df.columns
