import sys
from pathlib import Path

projeto_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(projeto_dir))

from catalog.src.application.usecase.get_product import GetProduct
from catalog.src.application.usecase.get_products import GetProducts
from catalog.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from catalog.src.infra.http.fast_api_adapter import FastApiAdapter
from catalog.src.infra.http.http_controller import HttpController
from catalog.src.infra.repository.product_repository_database import ProductRepositoryDatabase


def main() -> None:
    connection = AsyncPGAdapter()
    product_repository = ProductRepositoryDatabase(connection)
    get_product = GetProduct(product_repository)
    get_products = GetProducts(product_repository)
    http_server = FastApiAdapter()
    HttpController(http_server, get_product, get_products)
    http_server.listen(3004)


if __name__ == '__main__':
    main()
