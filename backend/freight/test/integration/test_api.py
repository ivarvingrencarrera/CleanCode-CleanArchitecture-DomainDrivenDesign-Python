from fastapi.encoders import jsonable_encoder

from freight.src.application.usecase.calculate_freight import Input, Item
from freight.src.infra.http.httpx_adapter import HttpxAdapter


async def test_calculate_freight() -> None:
    client = HttpxAdapter()
    input_ = Input(items=[Item(width=100, height=100, length=100, weight=3, quantity=3)])
    input_json = jsonable_encoder(input_)
    response = await client.post('http://localhost:3002/calculate_freight', input_json)
    output = response.json()
    status_code_ok = 200
    assert response.status_code == status_code_ok
    freight = 90
    assert output['freight'] == freight
