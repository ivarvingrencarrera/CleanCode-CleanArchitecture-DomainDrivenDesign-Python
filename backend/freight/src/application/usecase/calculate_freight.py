from pydantic import BaseModel

from freight.src.application.repository.zip_code_repository import ZIPCodeRepository
from freight.src.domain.entity.distance_calculator import DistanceCalculator
from freight.src.domain.entity.freight_calculator import FreightCalculator


class Item(BaseModel):
    width: int
    height: int
    length: int
    weight: float
    quantity: int


class Input(BaseModel):
    items: list[Item]
    origin: str | None = None
    destination: str | None = None


class Output(BaseModel):
    freight: float


class CalculateFreight:
    def __init__(self, zip_code_repository: ZIPCodeRepository) -> None:
        self.zip_code_repository = zip_code_repository

    async def execute(self, input_data: dict) -> dict:
        input_ = Input(**input_data)
        output = Output(freight=0)
        distance = 1000
        if input_.origin and input_.destination:
            origin = await self.zip_code_repository.get(input_.origin)
            destination = await self.zip_code_repository.get(input_.destination)
            if destination and origin:
                distance = DistanceCalculator.calculate(origin.coordinates, destination.coordinates)
        if input_.items:
            for item in input_.items:
                item_freight = FreightCalculator.calculate(
                    distance, item.width, item.height, item.length, item.weight, item.quantity
                )
                output.freight += item_freight
        return output.dict()
