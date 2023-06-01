from pydantic import BaseModel

from catalog.src.application.repository.product_repository import ProductRepository


class Output(BaseModel):
    id_product: int
    description: str
    price: float
    width: int
    height: int
    length: int
    weight: float
    currency: str
    volume: float
    density: float


class GetProduct:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, id_product: str) -> dict:
        product = await self.product_repository.get_product(id_product)
        return Output(
            id_product=product.id_product,
            description=product.description,
            price=product.price,
            width=product.width,
            height=product.height,
            length=product.length,
            weight=product.weight,
            currency=product.currency,
            volume=product.get_volume(),
            density=product.get_density(),
        ).dict()
