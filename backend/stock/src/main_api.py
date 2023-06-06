import sys
from pathlib import Path

projeto_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(projeto_dir))


from stock.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from stock.src.infra.repository.stock_entry_repository_database import StockEntryRepositoryDatabase
from stock.src.application.repository.stock_entry_repository import StockEntryRepository
from stock.src.application.usecase.calculate_stock import CalculateStock
from stock.src.application.usecase.decrement_stock import DecrementStock
from stock.src.infra.http.fast_api_adapter import FastApiAdapter
from stock.src.infra.http.http_controller import HttpController


def main() -> None:
    connection = AsyncPGAdapter()
    stock_entry_repository = StockEntryRepositoryDatabase(connection)
    decrement_stock = DecrementStock(stock_entry_repository)
    calculate_stock = CalculateStock(stock_entry_repository)
    http_server = FastApiAdapter()
    HttpController(http_server, decrement_stock, calculate_stock)
    http_server.listen(3007)


if __name__ == '__main__':
    main()
