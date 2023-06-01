from pydantic import BaseModel

from catalog.src.application.repository.product_repository import ProductRepository


class Output(BaseModel):
    id_product: int
    description: str
    price: float


class GetProducts:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, id_products: list) -> list[dict]:
        products = await self.product_repository.get_products(id_products)
        return [
            Output(
                id_product=product.id_product,
                description=product.description,
                price=product.price,
            ).dict()
            for product in products
        ]
