from checkout.src.application.repository.product_repository import ProductRepository
from checkout.src.domain.entity.product import Product
from checkout.src.infra.database.connection import Connection


class ProductRepositoryDatabase(ProductRepository):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def get_product(self, id_product: int) -> Product:
        product_query = 'SELECT * FROM ecommerce.product WHERE id_product = $1;'
        product_data = await self.connection.select_one(product_query, id_product)
        return Product(
            product_data.id_product,
            product_data.description,
            float(product_data.price),
            product_data.width,
            product_data.height,
            product_data.length,
            float(product_data.weight),
            product_data.currency,
        )
