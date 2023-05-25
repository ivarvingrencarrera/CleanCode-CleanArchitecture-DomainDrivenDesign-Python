import unittest

from checkout.src.domain.entity.freight_calculator import FreightCalculator
from checkout.src.domain.entity.product import Product


class TestFreightCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.product_single = Product(6, 'A', 1000, 100, 30, 10, 3, 'USD')
        self.product_multiple = Product(6, 'A', 1000, 100, 30, 10, 3, 'USD')
        self.product_minimum_price = Product(6, 'C', 1000, 10, 10, 10, 0.9, 'USD')

    def test_calculate_freight_for_single_item(self) -> None:
        freight = FreightCalculator.calculate(self.product_single)
        self.assertEqual(freight, 30)

    def test_calculate_freight_for_multiple_items(self) -> None:
        freight = FreightCalculator.calculate(self.product_multiple, 3)
        self.assertEqual(freight, 90)

    def test_calculate_freight_with_minimum_price(self) -> None:
        freight = FreightCalculator.calculate(self.product_minimum_price)
        self.assertEqual(freight, 10)


if __name__ == '__main__':
    unittest.main()
