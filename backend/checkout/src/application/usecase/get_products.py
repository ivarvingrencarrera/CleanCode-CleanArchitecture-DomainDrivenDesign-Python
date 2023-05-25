from pydantic import BaseModel

from checkout.src.application.repository.product_repository import ProductRepository


class Output(BaseModel):
    id_product: int
    description: str
    price: float


class GetProducts:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self) -> list[Output]:
        products = await self.product_repository.get_product()
        return [
            Output(
                id_product=product.id_product,
                description=product.description,
                price=product.price,
            )
            for product in products
        ]
