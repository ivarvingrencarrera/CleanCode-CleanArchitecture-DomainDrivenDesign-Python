from catalog.src.application.usecase.get_product import GetProduct
from catalog.src.application.usecase.get_products import GetProducts
from catalog.src.infra.http.http_server import HttpServer


class HttpController:
    def __init__(self, http_server: HttpServer, get_product: GetProduct, get_products: GetProducts) -> None:
        self.http_server = http_server
        self.get_product = get_product
        self.get_products = get_products

        self.http_server.on('get', '/products', self.get_products_handler)
        self.http_server.on('get', '/products/{id_product}', self.get_product_handler)

    async def get_products_handler(self, _: dict, body: list) -> list[dict]:
        return await self.get_products.execute(body)

    async def get_product_handler(self, params: dict, _: dict) -> dict:
        return await self.get_product.execute(params['id_product'])
