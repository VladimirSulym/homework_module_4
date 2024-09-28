import pytest

from main import Product, Category


@pytest.fixture()
def product_iphone ():
    return Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

@pytest.fixture()
def category_smartphone ():
    return Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                         [Product("Iphone 15", "512GB, Gray space", 210000.0, 8)])
