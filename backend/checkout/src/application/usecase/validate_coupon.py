from datetime import datetime

from checkout.src.application.repository.coupon_repository import CouponRepository


class ValidateCoupon:
    def __init__(self, coupon_repository: CouponRepository) -> None:
        self.coupon_repository = coupon_repository

    async def execute(self, code: str) -> bool:
        coupon = await self.coupon_repository.get_coupon(code)
        return not coupon.is_expired(datetime.now())
