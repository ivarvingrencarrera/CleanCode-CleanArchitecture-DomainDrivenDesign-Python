import pytest
from stock.src.application.usecase.calculate_stock import CalculateStock
from stock.src.application.usecase.decrement_stock import DecrementStock
from stock.src.application.repository.stock_entry_repository import StockEntryRepository

from stock.src.domain.entity.stock_entry import StockEntry


@pytest.fixture
def stock_entry_repository():
    stock_entries: list[StockEntry] = [
            StockEntry(1, "in", 20)

        ]

    class StockEntryRepositoryImp(StockEntryRepository):
        async def save(self, stock_entry: StockEntry) -> None:
            stock_entries.append(stock_entry)

        async def list(self, id_product: int) :
            return [stock_entry for stock_entry in stock_entries if stock_entry.id_product == id_product]

    return StockEntryRepositoryImp()



async def test_must_decrement_the_stock(stock_entry_repository) -> None:
    decrement_stock = DecrementStock(stock_entry_repository)
    input_ = {
        'items': [
            {'id_product': 1, 'quantity': 10},
            {'id_product': 2, 'quantity': 1},
            {'id_product': 3, 'quantity': 3}
        ]
    }
    await decrement_stock.execute(input_)
    calculate_stock = CalculateStock(stock_entry_repository)
    output = await calculate_stock.execute(1)    
    assert output['total'] == 10

    
