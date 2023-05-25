from pydantic import BaseModel

from checkout.src.application.repository.product_repository import ProductRepository
from checkout.src.domain.entity.freight_calculator import FreightCalculator
from checkout.src.domain.entity.product import Product


class Input(BaseModel):
    items: list


class Output(BaseModel):
    freight: float


class SimulateFreight:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    async def execute(self, input_: Input) -> Output:
        output = Output(freight=0)
        if input_.items:
            for item in input_.items:
                product: Product = await self.product_repository.get_product(item.id_product)
                item_freight = FreightCalculator.calculate(product, item.quantity)
                output.freight += item_freight
        return output
