from catalog.src.infra.http.request_adapter import RequestsAdapter

http_client = RequestsAdapter()


async def teste_sign_api() -> None:
    input_ = {
        'email': 'joao@gmail.com',
        'password': 'abc123',
    }
    url = 'http://localhost:3005/sign_up'
    await http_client.post(url, input_)
    url = 'http://localhost:3005/login'
    response = await http_client.post(url, input_)
    output = response.json()
    print(output['token'])

    url = 'http://localhost:3005/get_session'
    response = await http_client.post(url, output)
    output = response.json()
    assert output['email'] == 'joao@gmail.com'
