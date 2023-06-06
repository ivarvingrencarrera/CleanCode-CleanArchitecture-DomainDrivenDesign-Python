
from fastapi.encoders import jsonable_encoder
from checkout.src.application.gateway.stock_gateway import StockGateway, Input
from checkout.src.infra.http.http_client import HttpClient


class StockGatewayHttp(StockGateway):
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    async def decrement_stock(self, input_: Input) -> dict:
        input_json = jsonable_encoder(input_)
        response = await self.http_client.post('http://localhost:3007/decrement_stock', input_json)
        return response.json()
