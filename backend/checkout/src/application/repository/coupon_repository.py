from abc import ABC, abstractmethod

from checkout.src.domain.entity.coupon import Coupon


class CouponRepository(ABC):
    @abstractmethod
    async def get_coupon(self, code: str) -> Coupon:
        pass
