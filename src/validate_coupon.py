from datetime import datetime

from src.coupon_repository import CouponRepository
from src.coupon_repository_database import CouponRepositoryDatabase

class ValidateCoupon:
    def __init__(self, coupon_repository=None) -> None:
        self.coupon_repository: CouponRepository = coupon_repository or CouponRepositoryDatabase()

    async def execute(self, code: str) -> bool:
        coupon_data = await self.coupon_repository.get_coupon(code)
        return coupon_data.expire_date > datetime.now()
