from fastapi.encoders import jsonable_encoder

from freight.src.application.usecase.calculate_freight import CalculateFreight, Input, Item

calculate_freight = CalculateFreight()


async def test_calculate_freight() -> None:
    input_ = Input(
        items=[Item(width=100, height=100, length=100, weight=3, quantity=3)],
    )
    input_json = jsonable_encoder(input_)
    output = await calculate_freight.execute(input_json)
    freight = 90
    assert output['freight'] == freight
