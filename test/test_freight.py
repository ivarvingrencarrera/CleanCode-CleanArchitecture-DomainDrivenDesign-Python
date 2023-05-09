import unittest

from src.checkout import ProductData
from src.freight_calculator import FreightCalculator


class TestFreightCalculator(unittest.TestCase):
    def test_checkout_with_1_product_calculating_freight(self) -> None:
        product = ProductData(
            id_product=6,
            description='A',
            price=1000,
            width=100,
            height=30,
            length=10,
            weight=3,
            currency='USD',
        )
        freight = FreightCalculator.calculate(product)
        self.assertEqual(freight, 30)
