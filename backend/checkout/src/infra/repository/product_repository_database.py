from checkout.src.application.repository.product_repository import ProductRepository
from checkout.src.domain.entity.product import Product
from checkout.src.infra.database.connection import Connection


class ProductRepositoryDatabase(ProductRepository):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def get_product(self, id_product: int) -> Product:
        product_query = 'SELECT * FROM ecommerce.product WHERE id_product = $1;'
        product_data = await self.connection.select(product_query, id_product)
        product_row = product_data[0]
        return Product(
            product_row.id_product,
            product_row.description,
            float(product_row.price),
            product_row.width,
            product_row.height,
            product_row.length,
            float(product_row.weight),
            product_row.currency,
        )
