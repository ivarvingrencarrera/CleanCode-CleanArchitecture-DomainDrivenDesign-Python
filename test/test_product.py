import unittest

from src.domain.entity.product import Product


class TestProduct(unittest.TestCase):
    def test_must_not_create_a_product_with_invalid_dimensions(self):
        with self.assertRaises(ValueError) as context:
            Product(1, 'A', 1000, -50, 30, 10, 3, 'BRL')
        self.assertEqual(str(context.exception), 'Invalid dimension')
