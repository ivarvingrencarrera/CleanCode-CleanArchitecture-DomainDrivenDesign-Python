from catalog.src.application.repository.product_repository import ProductRepository
from catalog.src.domain.entity.product import Product
from catalog.src.infra.database.connection import Connection


class ProductRepositoryDatabase(ProductRepository):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def get_product(self, id_product: str) -> Product:
        product_query = 'SELECT * FROM ecommerce.product WHERE id_product = $1;'
        product_data = await self.connection.select(product_query, int(id_product))
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

    async def get_products(self, id_products: list) -> list[Product]:
        place_holders = ', '.join([f'${str(i + 1)}' for i in range(len(id_products))])
        product_query = f'SELECT * FROM ecommerce.product WHERE id_product IN ({place_holders});'
        products_data = await self.connection.select(product_query, *id_products)
        return [
            Product(
                product_data.id_product,
                product_data.description,
                float(product_data.price),
                product_data.width,
                product_data.height,
                product_data.length,
                float(product_data.weight),
                product_data.currency,
            )
            for product_data in products_data
        ]
