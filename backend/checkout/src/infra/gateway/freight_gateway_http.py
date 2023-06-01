from fastapi.encoders import jsonable_encoder
from checkout.src.application.gateway.freight_gateway import FreightGateway, Input, Output
from checkout.src.infra.http.http_client import HttpClient


class FreightGatewayHttp(FreightGateway):
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    async def calculate_freight(self, input_: Input) -> dict:
        input_json = jsonable_encoder(input_)
        response = await self.http_client.post('http://localhost:3002/calculate_freight', input_json)
        response.raise_for_status()
        return Output(**response.json())
