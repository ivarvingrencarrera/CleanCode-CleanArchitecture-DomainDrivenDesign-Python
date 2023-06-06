

from stock.src.infra.http.httpx_adapter import HttpxAdapter


http_client = HttpxAdapter()


async def teste_decrement_api() -> None:
    input_ = {
        'items': [
            {'id_product': 1, 'quantity': 10},
            {'id_product': 2, 'quantity': 1},
            {'id_product': 3, 'quantity': 3}
        ]
    }
    url = 'http://localhost:3007/decrement_stock'
    response = await http_client.post(url, input_)
    url = 'http://localhost:3007/calculate_stock'
    input_ = {'id_product': 1}
    response = await http_client.post(url, input_)
    output = response.json()
    assert output['total'] == 10
