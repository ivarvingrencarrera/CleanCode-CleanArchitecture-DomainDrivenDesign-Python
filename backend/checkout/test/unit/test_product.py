import unittest
from typing import Any

from parameterized import parameterized

from checkout.src.domain.entity.product import Product


class TestProduct(unittest.TestCase):
    @parameterized.expand(
        [
            (1, 'A', 1000, -50, 30, 10, 3, 'BRL'),  # invalid width
            (1, 'A', 1000, 50, -30, 10, 3, 'BRL'),  # invalid height
            (1, 'A', 1000, 50, 30, -10, 3, 'BRL'),  # invalid length
            (1, 'A', 1000, 50, 30, 10, -3, 'BRL'),  # invalid weight
        ]
    )
    def test_must_not_create_a_product_with_invalid_dimensions(self, *input_: Any) -> None:
        with self.assertRaises(ValueError) as context:
            Product(*input_)
        self.assertEqual(str(context.exception), 'Invalid dimension')


if __name__ == '__main__':
    unittest.main()
