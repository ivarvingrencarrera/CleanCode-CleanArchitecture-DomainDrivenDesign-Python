import os

import asyncpg
from dotenv import load_dotenv
from pydantic import BaseModel

from src.product_repository import ProductRepository

load_dotenv()
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


class ProductData(BaseModel):
    id_product: int
    description: str
    price: float
    width: int
    height: int
    length: int
    weight: float


class ProductRepositoryDatabase(ProductRepository):
    async def get_product(self, id_product: int) -> ProductData:
        async with asyncpg.create_pool(
            database=db_name, host=db_host, port=db_port, user=db_user, password=db_password
        ) as pool:
            async with pool.acquire() as connection:
                row = await connection.fetchrow(
                    'SELECT * FROM ecommerce.product WHERE id_product = $1;', id_product
                )
                return ProductData(
                    id_product=row[0],
                    description=row[1],
                    price=row[2],
                    width=row[3],
                    height=row[4],
                    length=row[5],
                    weight=row[6],
                )
