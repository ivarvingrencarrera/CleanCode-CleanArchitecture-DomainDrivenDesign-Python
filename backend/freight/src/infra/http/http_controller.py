from freight.src.application.usecase.calculate_freight import CalculateFreight
from freight.src.infra.http.http_server import HttpServer


class HttpController:
    def __init__(self, http_server: HttpServer, calculate_freight: CalculateFreight) -> None:
        self.http_server = http_server
        self.calculate_freight = calculate_freight

        self.http_server.on('post', '/calculate_freight', self.calculate_freight_handler)

    async def calculate_freight_handler(self, _: dict, body: dict) -> dict:
        return await self.calculate_freight.execute(body)
