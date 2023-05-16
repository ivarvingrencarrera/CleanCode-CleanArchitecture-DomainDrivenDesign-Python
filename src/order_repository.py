from abc import ABC, abstractmethod

from src.domain.entity.order import Order


class OrderRepository(ABC):
    @abstractmethod
    async def save(self, order: Order) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id_order: str) -> Order:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass
