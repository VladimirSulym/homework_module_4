from unittest.mock import patch

from main import fill_class_with_data, read_data_from_json


def test_product_init(product_iphone):
    assert product_iphone.name == "Iphone 15"
    assert product_iphone.description == "512GB, Gray space"
    assert product_iphone.price == 210000.0
    assert product_iphone.quantity == 8


def test_category_init(category_smartphone):
    assert category_smartphone.name == "Смартфоны"
    assert (
        category_smartphone.description
        == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert len(category_smartphone.products) == 1

    assert category_smartphone.category_count == 1
    assert category_smartphone.product_count == 1


@patch("main.Category")
def test_fill_class_with_data(mock_category, products_for_test):
    mock_category.return_value = 1
    assert fill_class_with_data(products_for_test) == [1, 1]


@patch("json.load")
@patch("builtins.open")
def test_read_data_from_json(mock_open, mock_load):
    mock_open.return_value.__iter__.return_value = []
    mock_load.return_value = 1
    assert read_data_from_json("products.json") == 1
