from stock.src.application.usecase.calculate_stock import CalculateStock
from stock.src.application.usecase.decrement_stock import DecrementStock
from stock.src.infra.http.http_server import HttpServer


class HttpController:
    def __init__(
        self,
        http_server: HttpServer,
        decrement_stock: DecrementStock,
        calculate_stock: CalculateStock,
    ) -> None:
        self.http_server = http_server
        self.decrement_stock = decrement_stock
        self.calculate_stock = calculate_stock

        self.http_server.on("post", "/decrement_stock", self.decrement_stock_handler)
        self.http_server.on("post", "/calculate_stock", self.calculate_stock_handler)

    async def decrement_stock_handler(self, _: dict, body: dict) -> dict:
        return await self.decrement_stock.execute(body)

    async def calculate_stock_handler(self, _: dict, body: dict) -> dict:
        return await self.calculate_stock.execute(body['id_product'])
