from collections.abc import AsyncGenerator

import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from freight.src.application.usecase.calculate_freight import Input, Item

STATUS_CODE_OK = 200
STATUS_CODE_UNPROCESSABLE_ENTITY = 422


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url='http://localhost:3002') as client:
        yield client


async def test_calculate_freight(client: AsyncClient) -> None:
    input_ = Input(items=[Item(width=100, height=100, length=100, weight=3, quantity=3)])
    input_json = jsonable_encoder(input_)
    response = await client.post('/calculate_freight', json=input_json)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    freight = 90
    assert output['freight'] == freight
