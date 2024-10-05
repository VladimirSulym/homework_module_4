from unittest.mock import patch

import pytest

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
    assert category_smartphone.products == ["Iphone 15, 210000.0 руб. Остаток: 8 шт."]

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


def test_new_product(product_for_new_product, capsys):
    assert product_for_new_product.name == "Samsung Galaxy S23 Ultra"
    assert (
        product_for_new_product.new_product(
            {
                "name": "Samsung Galaxy S23 Ultra",
                "description": "256GB, Серый цвет, 200MP камера",
                "price": 190000.0,
                "quantity": 5,
            }
        ).quantity
        == 10
    )
    assert (
        product_for_new_product.new_product(
            {
                "name": "Samsung Galaxy S23 Ultra",
                "description": "256GB, Серый цвет, 200MP камера",
                "price": 200000.0,
                "quantity": 5,
            }
        ).price
        == 200000.0
    )
    product_for_new_product.price = 0
    # captured = capsys.readouterr()
    # assert captured.out == "Цена не должна быть нулевая или отрицательная\n"


@patch("builtins.input")
def test_price_setter_y(mock_input, product_iphone):
    mock_input.return_value = "y"
    product_iphone.price = 100.0
    assert product_iphone.price == 100.0


@patch("builtins.input")
def test_price_setter_n(mock_input, product_iphone):
    mock_input.return_value = "n"
    product_iphone.price = 100.0
    assert product_iphone.price == 210000.0


def test_price_setter(product_iphone):
    product_iphone.price = 300000.0
    assert product_iphone.price == 300000.0


def test_add_product(category_smartphone, product_iphone):
    category_smartphone.add_product(product_iphone)
    assert category_smartphone.product_count == 3


def test_product_str(product_iphone):
    assert str(product_iphone) == "Product(Iphone 15, 512GB, Gray space, 210000.0, 8)"
    # assert str(product_iphone) == "Iphone 15, 210000.0 руб. Остаток: 8 шт."


def test_product_add(product_iphone):
    assert product_iphone + product_iphone == 3360000


def test_category_str(category_smartphone):
    assert str(category_smartphone) == "Смартфоны, количество продуктов: 8 шт."


def test_add_typeerror(product_smartphone, product_lawn_grass):
    with pytest.raises(TypeError) as exc_info:
        product_smartphone + product_lawn_grass
    assert exc_info.type == TypeError


def test_add_product_typeerror(category_smartphone):
    with pytest.raises(TypeError) as exc_info:
        category_smartphone.add_product("Not a product")
    assert exc_info.type == TypeError
