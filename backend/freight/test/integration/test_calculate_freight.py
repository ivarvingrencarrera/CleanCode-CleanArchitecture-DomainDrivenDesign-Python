from freight.src.application.usecase.calculate_freight import CalculateFreight, Input, Item

calculate_freight = CalculateFreight()


async def test_calculate_freight() -> None:
    input_ = Input(
        items=[Item(width=100, height=100, length=100, weight=3, quantity=3)],
    )
    output = await calculate_freight.execute(input_)
    freight = 90
    assert output['freight'] == freight
