import pytest

from catalog.src.infra.http.fast_api_adapter import jsonable_encoder
from catalog.src.infra.http.request_adapter import RequestsAdapter

http_client = RequestsAdapter()


async def test_get_products() -> None:
    input_ = [1, 2, 3]
    body = jsonable_encoder(input_)
    url = 'http://localhost:3004/products/'
    response = await http_client.get(url, body)
    output = response.json()
    status_code_ok = 200
    assert response.status_code == status_code_ok
    assert len(output) == 3


async def test_get_product_1() -> None:
    input_ = 1
    url = f'http://localhost:3004/products/{input_}'
    body: dict = {}
    response = await http_client.get(url, body)
    output = response.json()
    status_code_ok = 200
    assert response.status_code == status_code_ok
    assert output['id_product'] == 1
    assert output['description'] == 'A'
    assert output['price'] == 1000
    assert output['volume'] == 0.03
    assert output['density'] == 0.01


async def test_get_product_with_invalid_dimensions() -> None:
    product_id = 4
    url = f'http://localhost:3004/products/{product_id}'
    body: dict = {}
    with pytest.raises(ValueError, match='Invalid dimension'):
        await http_client.get(url, body)
