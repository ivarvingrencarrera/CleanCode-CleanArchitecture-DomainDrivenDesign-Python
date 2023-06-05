from abc import ABC, abstractmethod

from pydantic import BaseModel


class Item(BaseModel):
    width: int
    height: int
    length: int
    weight: float
    quantity: int


class Input(BaseModel):
    items: list[Item]
    origin: str = None
    destination: str = None


class Output(BaseModel):
    freight: float


class FreightGateway(ABC):
    @abstractmethod
    async def calculate_freight(self, input_: Input) -> Output:
        pass
