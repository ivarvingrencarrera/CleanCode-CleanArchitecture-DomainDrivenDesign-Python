from checkout.src.application.gateway.catalog_gateway import CatalogGateway
from checkout.src.domain.entity.product import Product
from fastapi.encoders import jsonable_encoder

from checkout.src.infra.http.http_client import HttpClient


class CatalogGatewayHttp(CatalogGateway):
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    async def get_products(self, ids_products) -> list[Product]:    
        url = 'http://localhost:3004/products/'
        response = await self.http_client.get(url, jsonable_encoder(ids_products))
        return [Product(**product) for product in response.json()]

    async def get_product(self, id_product) -> Product:
        url = f'http://localhost:3004/products/{id_product}'
        response = await self.http_client.get(url, id_product)
        return Product(**response.json())