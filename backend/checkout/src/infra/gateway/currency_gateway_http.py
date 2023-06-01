from checkout.src.application.gateway.currency_gateway import CurrencyGateway
from checkout.src.infra.http.http_client import HttpClient


class CurrencyGatewayHttp(CurrencyGateway):
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    async def get_currencies(self) -> dict:
        response = await self.http_client.get('http://localhost:3003/currencies', {})
        response.raise_for_status()
        return response.json()
