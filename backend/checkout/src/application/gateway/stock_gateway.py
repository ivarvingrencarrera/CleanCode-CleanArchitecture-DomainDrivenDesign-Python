from abc import ABC, abstractmethod

from pydantic import BaseModel


class Item(BaseModel):
    id_product: int
    quantity: int

class Input(BaseModel):
    items: list[Item]

class StockGateway(ABC):
    @abstractmethod
    async def decrement_stock(input: Input) -> None:
        pass
