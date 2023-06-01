from catalog.src.application.usecase.get_products import GetProducts
from catalog.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from catalog.src.infra.repository.product_repository_database import ProductRepositoryDatabase

connection = AsyncPGAdapter()
product_repository = ProductRepositoryDatabase(connection)
get_products = GetProducts(product_repository)


async def test_get_products() -> None:
    product_ids = [1, 2, 3]
    output = await get_products.execute(product_ids)
    assert len(output) == 3
