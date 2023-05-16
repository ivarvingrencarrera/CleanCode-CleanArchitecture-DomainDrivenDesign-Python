from pydantic import BaseModel

from src.domain.entity.freight_calculator import FreightCalculator
from src.domain.entity.product import Product
from src.product_repository import ProductRepository
from src.product_repository_database import ProductRepositoryDatabase


class Input(BaseModel):
    items: list


class Output(BaseModel):
    freight: float


class SimulateFreight:
    def __init__(self, product_repository: ProductRepository | None = None) -> None:
        self.product_repository = product_repository or ProductRepositoryDatabase()

    async def execute(self, input_: Input) -> Output:
        output = Output(freight=0)
        if input_.items:
            for item in input_.items:
                product: Product = await self.product_repository.get_product(item.id_product)
                item_freight = FreightCalculator.calculate(product)
                output.freight += max(item_freight, 10) * item.quantity
        return output
