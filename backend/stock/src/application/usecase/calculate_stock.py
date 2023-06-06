from pydantic import BaseModel
from stock.src.domain.entity.stock_calculator import StockCalculator
from stock.src.application.repository.stock_entry_repository import StockEntryRepository


class Output(BaseModel):
    total: int

class CalculateStock:
    def __init__(self, stock_entry_repository: StockEntryRepository) -> None:
        self.stock_entry_repository = stock_entry_repository

    async def execute(self, id_product: int) -> dict:
        stock_entries = await self.stock_entry_repository.list(id_product)
        total = StockCalculator.calculate(stock_entries)
        return Output(total=total).dict()