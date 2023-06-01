from abc import ABC, abstractmethod

from catalog.src.domain.entity.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def get_product(self, id_product: str) -> Product:
        pass

    @abstractmethod
    async def get_products(self, id_products: list) -> list[Product]:
        pass
