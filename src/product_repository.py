from abc import ABC, abstractmethod

from src.domain.entity.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def get_product(self, id_product: int) -> Product:
        pass
