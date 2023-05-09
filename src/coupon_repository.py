from abc import ABC, abstractmethod


class CouponRepository(ABC):
    @abstractmethod
    async def get_coupon(self, code: str) -> None:
        pass
