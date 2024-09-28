import pytest

def test_product_init(product_iphone):
    assert product_iphone.name == "Iphone 15"
    assert product_iphone.description == "512GB, Gray space"
    assert product_iphone.price == 210000.0
    assert product_iphone.quantity == 8

def test_category_init(category_smartphone):
    assert category_smartphone.name == "Смартфоны"
    assert category_smartphone.description == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    assert len(category_smartphone.products) == 1

    assert category_smartphone.category_count == 1
    assert category_smartphone.product_count == 1
