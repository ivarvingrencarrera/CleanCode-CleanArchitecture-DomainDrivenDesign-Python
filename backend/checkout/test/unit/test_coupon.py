import unittest
from datetime import datetime

from checkout.src.domain.entity.coupon import Coupon


class TestCoupon(unittest.TestCase):
    def setUp(self) -> None:
        self.coupon_valid = Coupon('VALE20', 20, datetime(2023, 10, 1, 10, 0, 0))
        self.coupon_invalid = Coupon('VALE10', 10, datetime(2022, 10, 1, 10, 0, 0))
        self.today = datetime(2023, 5, 1, 10, 0, 0)

    def test_must_create_valid_discount_coupon(self) -> None:
        self.assertEqual(self.coupon_valid.is_expired(self.today), False)

    def test_must_create_invalid_discount_coupon(self) -> None:
        self.assertEqual(self.coupon_invalid.is_expired(self.today), True)

    def test_must_calculate_discount(self) -> None:
        self.assertEqual(self.coupon_valid.calculate_discount(1000), 200)


if __name__ == '__main__':
    unittest.main()
