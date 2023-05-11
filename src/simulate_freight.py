from pydantic import BaseModel

from src.product_repository import ProductRepository
from src.product_repository_database import ProductData, ProductRepositoryDatabase


class Item(BaseModel):
    id_product: int
    quantity: int


class Input(BaseModel):
    items: list[Item]


class Output(BaseModel):
    freight: float


class SimulateFreight:
    def __init__(self, product_repository=None) -> None:
        self.product_repository: ProductRepository = (
            product_repository or ProductRepositoryDatabase()
        )

    async def execute(self, input_: Input) -> Output:
        output = Output(freight=0)
        if input_.items:
            for item in input_.items:
                product_data: ProductData = await self.product_repository.get_product(
                    item.id_product
                )
                volume = (
                    product_data.width / 100 * product_data.height / 100 * product_data.length / 100
                )
                density = product_data.weight / volume
                item_freight = 1000 * volume * (density / 100)
                output.freight += max(item_freight, 10) * item.quantity
        return output
