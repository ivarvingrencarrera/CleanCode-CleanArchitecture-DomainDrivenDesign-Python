from src.application.usecase.simulate_freight import Input, SimulateFreight
from src.domain.entity.item import Item

simulate_freight = SimulateFreight()


async def test_freight_with_3_products() -> None:
    input_ = Input(
        items=[
            Item(id_product=1, quantity=1),
            Item(id_product=2, quantity=1),
            Item(id_product=3, quantity=3),
        ],
        origin='22060030',
        destination='88015600',
    )
    output = await simulate_freight.execute(input_)
    freight = 280
    assert output.freight == freight
