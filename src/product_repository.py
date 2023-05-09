from abc import ABC, abstractmethod


class ProductRepository(ABC):
    @abstractmethod
    async def get_product(self, id_product: int) -> None:
        pass
