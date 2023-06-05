import unittest

from freight.src.domain.entity.freight_calculator import FreightCalculator


class TestFreightCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.product_single = (100, 30, 10, 3)
        self.product_multiple = (100, 30, 10, 3, 3)
        self.product_minimum_price = (10, 10, 10, 0.9)

    def test_calculate_freight_for_single_item(self) -> None:
        freight = FreightCalculator.calculate(1000, 100, 30, 10, 3)
        self.assertEqual(freight, 30)

    def test_calculate_freight_for_multiple_items(self) -> None:
        freight = FreightCalculator.calculate(1000, 100, 30, 10, 3, 3)
        self.assertEqual(freight, 90)

    def test_calculate_freight_with_minimum_price(self) -> None:
        freight = FreightCalculator.calculate(1000, 10, 10, 10, 0.9)
        self.assertEqual(freight, 10)


if __name__ == '__main__':
    unittest.main()
