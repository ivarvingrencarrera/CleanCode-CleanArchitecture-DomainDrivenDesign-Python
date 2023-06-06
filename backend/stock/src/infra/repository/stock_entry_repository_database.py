from stock.src.domain.entity.stock_entry import StockEntry
from stock.src.application.repository.stock_entry_repository import StockEntryRepository
from stock.src.infra.database.connection import Connection


class StockEntryRepositoryDatabase(StockEntryRepository):
    stock_entries: list[StockEntry] = [
                StockEntry(1, "in", 20)
            ]
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def save(self, stock_entry: StockEntry) -> None:
        self.stock_entries.append(stock_entry)

    async def list(self, id_product: int) :
        return [stock_entry for stock_entry in self.stock_entries if stock_entry.id_product == id_product]
