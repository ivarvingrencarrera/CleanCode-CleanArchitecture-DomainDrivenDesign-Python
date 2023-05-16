import unittest
import uuid
from datetime import datetime

from src.domain.entity.currency_table import CurrencyTable
from src.domain.entity.order import Order
from src.domain.entity.product import Product


class TestOrder(unittest.TestCase):
    def setUp(self) -> None:
        self.uuid_ = uuid.uuid4().hex
        self.cpf = '353.775.320-90'
        self.currency_table = CurrencyTable()

    def test_must_not_create_an_order_with_invalid_cpf(self) -> None:
        invalid_cpf = '406.302.170-27'
        with self.assertRaises(ValueError) as context:
            Order(self.uuid_, invalid_cpf)
        self.assertEqual(str(context.exception), 'Invalid cpf')

    def test_must_not_add_duplicate_item(self):
        order = Order(self.uuid_, self.cpf)
        order.add_item(Product(1, 'A', 1000, 50, 30, 10, 3, 'BRL'), 1)
        with self.assertRaises(ValueError) as context:
            order.add_item(Product(1, 'A', 1000, 50, 30, 10, 3, 'BRL'), 1)
        self.assertEqual(str(context.exception), 'Duplicated item')

    def test_must_not_add_item_with_negative_quantity(self):
        order = Order(self.uuid_, self.cpf)
        with self.assertRaises(ValueError) as context:
            order.add_item(Product(1, 'A', 1000, 50, 30, 10, 3, 'BRL'), -1)
        self.assertEqual(str(context.exception), 'Invalid quantity')

    def test_must_create_an_empty_order(self):
        order = Order(self.uuid_, self.cpf)
        self.assertEqual(order.get_total(), 0)

    def test_must_create_an_order_with_three_items(self):
        order = Order(self.uuid_, self.cpf)
        order.add_item(Product(1, 'A', 1000, 50, 30, 10, 3, 'BRL'), 1)
        order.add_item(Product(2, 'B', 5000, 50, 50, 50, 22, 'BRL'), 1)
        order.add_item(Product(3, 'C', 30, 10, 10, 10, 0.9, 'BRL'), 3)
        self.assertEqual(order.get_total(), 6090)

    def test_must_create_an_order_with_item_in_dollar(self):
        self.currency_table.add_currency('USD', 3)
        order = Order(self.uuid_, self.cpf, self.currency_table)
        order.add_item(Product(6, 'A', 1000, 100, 30, 10, 3, 'USD'), 1)
        self.assertEqual(order.get_total(), 3000)

    def test_must_create_an_order_and_generate_the_code(self):
        date = datetime(2023, 10, 1, 10, 0, 0)
        order = Order(self.uuid_, self.cpf, self.currency_table, 1, date)
        order.add_item(Product(1, 'A', 1000, 50, 30, 10, 3, 'BRL'), 1)
        order.add_item(Product(2, 'B', 5000, 50, 50, 50, 22, 'BRL'), 1)
        order.add_item(Product(3, 'C', 30, 10, 10, 10, 0.9, 'BRL'), 3)
        self.assertEqual(order.get_code(), '202300000001')
