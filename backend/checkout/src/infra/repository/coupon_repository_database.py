from checkout.src.application.repository.coupon_repository import CouponRepository
from checkout.src.domain.entity.coupon import Coupon
from checkout.src.infra.database.connection import Connection


class CouponRepositoryDatabase(CouponRepository):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def get_coupon(self, coupon: str) -> Coupon:
        coupon_data = await self.connection.select('SELECT * FROM ecommerce.coupon WHERE code = $1;', coupon)
        coupon_row = coupon_data[0]
        return Coupon(coupon_row.code, float(coupon_row.percentage), coupon_row.expire_date)
