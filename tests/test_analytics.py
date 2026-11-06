import pandas as pd
import pytest
import json

from backend.analytics import (
    calculate_total_revenue,
    calculate_average_order_value,
    calculate_total_orders,
    get_top_selling_products,
    get_top_revenue_products,
    generate_sales_summary
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


def test_generate_sales_summary():

    df = pd.DataFrame({
        "Invoice": ["INV001", "INV001", "INV002"],
        "StockCode": ["A01", "B02", "A01"],
        "Description": ["Kalem", "Defter", "Kalem"],
        "Quantity": [2, 1, 3],
        "Price": [10.0, 50.0, 10.0]
    })

    result = generate_sales_summary(df)

    assert isinstance(result, dict)

    assert result["total_revenue"] == 100.0
    assert result["average_order_value"] == 50.0
    assert result["total_orders"] == 2

    assert len(result["top_revenue_products"]) == 2

    assert result["top_revenue_products"][0]["StockCode"] == "A01"
    assert result["top_revenue_products"][0]["Revenue"] == 50.0


def test_generate_sales_summary_json_serializable():

    df = pd.DataFrame({
        "Invoice": ["INV001", "INV002"],
        "StockCode": ["A01", "B02"],
        "Description": ["Kalem", "Defter"],
        "Quantity": [5, 2],
        "Price": [10.0, 25.0]
    })

    summary = generate_sales_summary(df)

    json_output = json.dumps(summary, allow_nan=False)

    assert isinstance(json_output, str)

    parsed_summary = json.loads(json_output)

    assert parsed_summary["total_revenue"] == 100.0
    assert len(parsed_summary["top_revenue_products"]) == 2


def test_generate_sales_summary_metrics_consistency():

    df = pd.DataFrame({
        "Invoice": ["INV001", "INV001", "INV002"],
        "StockCode": ["A01", "B02", "C03"],
        "Description": ["Kalem", "Defter", "Silgi"],
        "Quantity": [2, 1, 4],
        "Price": [10.0, 50.0, 5.0]
    })

    summary = generate_sales_summary(df)

    expected_average = round(
        summary["total_revenue"] / summary["total_orders"],
        2
    )

    assert summary["average_order_value"] == expected_average


def test_generate_sales_summary_empty_dataframe():

    df = pd.DataFrame(columns=[
        "Invoice",
        "StockCode",
        "Description",
        "Quantity",
        "Price"
    ])

    summary = generate_sales_summary(df)

    assert summary["total_revenue"] == 0.0
    assert summary["average_order_value"] == 0.0
    assert summary["total_orders"] == 0
    assert summary["top_revenue_products"] == []


def test_generate_sales_summary_does_not_modify_original():

    df = pd.DataFrame({
        "Invoice": ["INV001", "INV002"],
        "StockCode": ["A01", "B02"],
        "Description": ["Kalem", "Defter"],
        "Quantity": [5, 2],
        "Price": [10.0, 25.0]
    })

    original_df = df.copy(deep=True)

    generate_sales_summary(df)

    pd.testing.assert_frame_equal(df, original_df)


def test_generate_sales_summary_schema():

    df = pd.DataFrame({
        "Invoice": ["INV001", "INV002"],
        "StockCode": ["A01", "B02"],
        "Description": ["Kalem", "Defter"],
        "Quantity": [5, 2],
        "Price": [10.0, 25.0]
    })

    summary = generate_sales_summary(df)

    expected_keys = {
        "total_revenue",
        "average_order_value",
        "total_orders",
        "top_revenue_products"
    }

    assert set(summary.keys()) == expected_keys

    assert isinstance(summary["total_revenue"], float)
    assert isinstance(summary["average_order_value"], float)
    assert isinstance(summary["total_orders"], int)
    assert isinstance(summary["top_revenue_products"], list)


def test_generate_sales_summary_missing_price_column():

    df = pd.DataFrame({
        "Invoice": ["INV001", "INV002"],
        "StockCode": ["A01", "B02"],
        "Description": ["Kalem", "Defter"],
        "Quantity": [5, 2]
    })

    with pytest.raises(ValueError, match="Price"):
        generate_sales_summary(df)


@pytest.mark.parametrize(
    "missing_column",
    [
        "Invoice",
        "StockCode",
        "Description",
        "Quantity",
        "Price"
    ]
)
def test_generate_sales_summary_missing_required_columns(
    missing_column
):
    df = pd.DataFrame({
        "Invoice": ["INV001", "INV002"],
        "StockCode": ["A01", "B02"],
        "Description": ["Kalem", "Defter"],
        "Quantity": [5, 2],
        "Price": [10.0, 25.0]
    })

    df = df.drop(columns=[missing_column])

    with pytest.raises(ValueError, match=missing_column):
        generate_sales_summary(df)
