from stock.src.domain.entity.stock_entry import StockEntry


class StockEntryRepository():

    async def save(self, stock_entry: StockEntry) -> None:
        pass

    async def list(self, id_product: int) -> list[StockEntry]:
        pass