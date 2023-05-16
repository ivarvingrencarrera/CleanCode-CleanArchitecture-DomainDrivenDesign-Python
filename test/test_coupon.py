import unittest

from src.domain.entity.coupon import Coupon


class TestCoupon(unittest.TestCase):
    def test_must_create_a_valid_discount_coupon(self):
        coupon = Coupon('VALE20', 20, '2023-10-01T10:00:00')
        self.assertEqual(coupon.is_expired('2023-09-01T10:00:00'), False)

    def test_must_create_a_invalid_discount_coupon(self):
        coupon = Coupon('VALE20', 20, '2023-10-01T10:00:00')
        self.assertEqual(coupon.is_expired('2024-10-01T10:00:00'), True)

    def test_must_calculate_the_discount(self):
        coupon = Coupon('VALE20', 20, '2023-10-01T10:00:00')
        self.assertEqual(coupon.calculate_discount(1000), 200)
