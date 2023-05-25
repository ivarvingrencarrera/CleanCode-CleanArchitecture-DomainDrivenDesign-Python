import unittest
import uuid
from datetime import datetime

from checkout.src.domain.entity.currency_table import CurrencyTable
from checkout.src.domain.entity.order import Order
from checkout.src.domain.entity.product import Product


class TestOrder(unittest.TestCase):
    def setUp(self) -> None:
        self.uuid_ = uuid.uuid4().hex
        self.cpf = '353.775.320-90'
        self.currency_table = CurrencyTable()
        self.product_a = Product(1, 'A', 1000, 50, 30, 10, 3, 'BRL')
        self.product_b = Product(2, 'B', 5000, 50, 50, 50, 22, 'BRL')
        self.product_c = Product(3, 'C', 30, 10, 10, 10, 0.9, 'BRL')

    def test_invalid_cpf(self) -> None:
        invalid_cpf = '406.302.170-27'
        with self.assertRaises(ValueError) as context:
            Order(self.uuid_, invalid_cpf)
        self.assertEqual(str(context.exception), 'Invalid cpf')

    def test_duplicate_item(self) -> None:
        order = Order(self.uuid_, self.cpf)
        order.add_item(self.product_a, 1)
        with self.assertRaises(ValueError) as context:
            order.add_item(self.product_a, 1)
        self.assertEqual(str(context.exception), 'Duplicated item')

    def test_negative_quantity(self) -> None:
        order = Order(self.uuid_, self.cpf)
        with self.assertRaises(ValueError) as context:
            order.add_item(self.product_a, -1)
        self.assertEqual(str(context.exception), 'Invalid quantity')

    def test_empty_order(self) -> None:
        order = Order(self.uuid_, self.cpf)
        self.assertEqual(order.get_total(), 0)

    def test_order_with_three_items(self) -> None:
        order = Order(self.uuid_, self.cpf)
        order.add_item(self.product_a, 1)
        order.add_item(self.product_b, 1)
        order.add_item(self.product_c, 3)
        self.assertEqual(order.get_total(), 6090)

    def test_order_with_item_in_dollar(self) -> None:
        self.currency_table.add_currency('USD', 3)
        order = Order(self.uuid_, self.cpf, self.currency_table)
        order.add_item(Product(6, 'A', 1000, 100, 30, 10, 3, 'USD'), 1)
        self.assertEqual(order.get_total(), 3000)

    def test_order_and_generate_code(self) -> None:
        date = datetime(2023, 10, 1, 10, 0, 0)
        order = Order(self.uuid_, self.cpf, self.currency_table, 1, date)
        order.add_item(self.product_a, 1)
        order.add_item(self.product_b, 1)
        order.add_item(self.product_c, 3)
        self.assertEqual(order.get_code(), '202300000001')
