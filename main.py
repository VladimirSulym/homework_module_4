import json
import os
from abc import ABC, abstractmethod


class BaseProduct(ABC):
    @abstractmethod
    def new_product(cls, value):
        pass

    @abstractmethod
    def price(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class MixinLog:
    def __init__(self, name, description, price, quantity):
        print(self)
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})"


class Product(MixinLog, BaseProduct):
    __product_list = []
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__(name, description, price, quantity)

    # def __str__(self):
    #     return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) is type(other):
            return self.quantity * self.price + other.quantity * other.price
        else:
            raise TypeError

    @classmethod
    def new_product(cls, value):
        name, description, price, quantity = value.values()
        for index, product in enumerate(Product.__product_list):
            if product["name"] == name:
                Product.__product_list[index]["quantity"] = product["quantity"] + quantity
                if product["price"] < price:
                    Product.__product_list[index]["price"] = price
            return cls(product["name"], product["description"], product["price"], product["quantity"])
        Product.__product_list.append({"name": name, "description": description, "price": price, "quantity": quantity})
        return cls(name, description, price, quantity)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print(str("Цена не должна быть нулевая или отрицательная"))
        elif 0 < value < self.__price:
            if input("подтвердите понижение цены y / n => ") == "y":
                self.__price = value
        else:
            self.__price = value


class Category:
    name: str
    description: str
    products: list
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products) if products else 0

    def __str__(self):
        number_of_products = 0
        for product in self.__products:
            number_of_products += product.quantity
        return f"{self.name}, количество продуктов: {number_of_products} шт."

    def middle_price(self):
        try:
            all_price = 0
            for product in self.__products:
                all_price += product.price
            return all_price / Category.product_count
        except ZeroDivisionError or TypeError:
            return 0
    def add_product(self, value):
        if isinstance(value, Product):
            self.__products.append(value)
            Category.product_count += 1
        else:
            raise TypeError

    @property
    def products(self):
        result = []
        for product in self.__products:
            result.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
        return result


path_file_date = os.path.join(os.path.dirname(__file__), "data", "products.json")


def read_data_from_json(path):
    with open(path, "r", encoding="UTF-8") as f:
        data = json.load(f)
        return data


def fill_class_with_data(categories):
    result = []
    for category in categories:
        products = []
        for product in category["products"]:
            products.append(Product(**product))
        category["products"] = products
        result.append(Category(**category))
    return result


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


if __name__ == '__main__':
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())