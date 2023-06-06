from pydantic import BaseModel
from stock.src.application.repository.stock_entry_repository import StockEntryRepository
from stock.src.domain.entity.stock_entry import StockEntry

class Item(BaseModel):
    id_product: int
    quantity: int

class Input(BaseModel):
    items: list[Item]


class DecrementStock:
    def __init__(self, stock_entry_repository: StockEntryRepository) -> None:
        self.stock_entry_repository = stock_entry_repository

    async def execute(self, input_data: dict) -> None:
        input_ = Input(**input_data)
        for item in input_.items:
            await self.stock_entry_repository.save(StockEntry(item.id_product, "out", item.quantity))