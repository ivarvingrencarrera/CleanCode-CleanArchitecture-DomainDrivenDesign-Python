from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient

from src.main import app

STATUS_CODE_OK = 200


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.mark.asyncio
async def test_checkout_with_invalid_cpf(client: AsyncClient) -> None:
    input_ = {'cpf': '406.302.170-27'}
    response = await client.post('/checkout', json=input_)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    assert output['message'] == 'Invalid cpf'


@pytest.mark.asyncio
async def test_empty_checkout(client: AsyncClient) -> None:
    input_ = {'cpf': '353.775.320-90'}
    response = await client.post('/checkout', json=input_)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    assert output['total'] == 0


@pytest.mark.asyncio
async def test_checkout_with_3_products(client: AsyncClient) -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [
            {'id_product': 1, 'quantity': 1},
            {'id_product': 2, 'quantity': 1},
            {'id_product': 3, 'quantity': 3},
        ],
    }
    response = await client.post('/checkout', json=input_)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    total = 6090
    assert output['total'] == total


@pytest.mark.asyncio
async def test_checkout_with_3_products_with_coupon(client: AsyncClient) -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [
            {'id_product': 1, 'quantity': 1},
            {'id_product': 2, 'quantity': 1},
            {'id_product': 3, 'quantity': 3},
        ],
        'coupon': 'VALE20',
    }
    response = await client.post('/checkout', json=input_)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    total = 4872
    assert output['total'] == total

@pytest.mark.asyncio
async def test_checkout_with_3_products_with_invalid_coupon(client: AsyncClient) -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [
            {'id_product': 1, 'quantity': 1},
            {'id_product': 2, 'quantity': 1},
            {'id_product': 3, 'quantity': 3},
        ],
        'coupon': 'VALE10',
    }
    response = await client.post('/checkout', json=input_)
    output = response.json()
    assert response.status_code == STATUS_CODE_OK
    total = 6090
    assert output['total'] == total
