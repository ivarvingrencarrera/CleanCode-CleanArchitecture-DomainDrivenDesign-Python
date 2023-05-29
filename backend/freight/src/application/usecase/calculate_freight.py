from pydantic import BaseModel

from freight.src.domain.entity.freight_calculator import FreightCalculator


class Item(BaseModel):
    width: int
    height: int
    length: int
    weight: float
    quantity: int


class Input(BaseModel):
    items: list[Item]


class Output(BaseModel):
    freight: float


class CalculateFreight:
    def __init__(self) -> None:
        pass

    async def execute(self, input_: Input) -> dict:
        output = Output(freight=0)
        if input_.items:
            for item in input_.items:
                item_freight = FreightCalculator.calculate(
                    item.width, item.height, item.length, item.weight, item.quantity
                )
                output.freight += item_freight
        return output.dict()
