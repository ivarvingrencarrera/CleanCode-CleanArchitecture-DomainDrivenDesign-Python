from abc import ABC, abstractmethod


class OrderRepository(ABC):
    @abstractmethod
    async def save(self, order) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id_order: str) -> None:
        pass

    @abstractmethod
    async def count(self) -> None:
        pass
