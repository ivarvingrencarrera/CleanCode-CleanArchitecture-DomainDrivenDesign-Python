from abc import ABC, abstractmethod
from checkout.src.domain.entity.product import Product

class CatalogGateway(ABC):
    @abstractmethod
    async def get_product(id_product) -> Product:
        pass

    @abstractmethod
    async def get_products(id_products) -> list[Product]:
        pass
