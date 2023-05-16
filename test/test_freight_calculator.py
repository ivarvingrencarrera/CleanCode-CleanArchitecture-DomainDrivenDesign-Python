import unittest

from src.domain.entity.freight_calculator import FreightCalculator
from src.domain.entity.product import Product


class TestFreightCalculator(unittest.TestCase):
    def test_must_calculate_product_freight(self) -> None:
        product = Product(6, 'A', 1000, 100, 30, 10, 3, 'USD')
        freight = FreightCalculator.calculate(product)
        self.assertEqual(freight, 30)
