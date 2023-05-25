from checkout.src.application.repository.coupon_repository import CouponRepository
from checkout.src.domain.entity.coupon import Coupon
from checkout.src.infra.database.connection import Connection


class CouponRepositoryDatabase(CouponRepository):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def get_coupon(self, coupon: str) -> Coupon:
        coupon_data = await self.connection.select_one('SELECT * FROM ecommerce.coupon WHERE code = $1;', coupon)
        return Coupon(coupon_data.code, float(coupon_data.percentage), coupon_data.expire_date)
