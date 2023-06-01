from catalog.src.application.usecase.get_product import GetProduct
from catalog.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from catalog.src.infra.http.fast_api_adapter import jsonable_encoder
from catalog.src.infra.repository.product_repository_database import ProductRepositoryDatabase

connection = AsyncPGAdapter()
product_repository = ProductRepositoryDatabase(connection)
get_product = GetProduct(product_repository)


async def test_get_product() -> None:
    input_ = 1
    input_json = jsonable_encoder(input_)
    output = await get_product.execute(input_json)
    assert output['id_product'] == 1
    assert output['description'] == 'A'
    assert output['price'] == 1000
    assert output['width'] == 100
    assert output['height'] == 30
    assert output['length'] == 10
    assert output['weight'] == 3
    assert output['currency'] == 'BRL'
    assert output['volume'] == 0.03
    assert output['density'] == 0.01
