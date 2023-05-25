from checkout.src.application.usecase.simulate_freight import Input, SimulateFreight
from checkout.src.domain.entity.item import Item
from checkout.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from checkout.src.infra.repository.product_repository_database import ProductRepositoryDatabase

connection = AsyncPGAdapter()
product_repository = ProductRepositoryDatabase(connection)
simulate_freight = SimulateFreight(product_repository)


async def test_freight_with_3_products() -> None:
    input_ = Input(
        items=[
            Item(1, 1, 1000, 'BRL'),
            Item(2, 1, 5000, 'BRL'),
            Item(3, 3, 30, 'BRL'),
        ],
        origin='22060030',
        destination='88015600',
    )
    output = await simulate_freight.execute(input_)
    freight = 280
    assert output.freight == freight
