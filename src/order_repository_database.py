import os

import asyncpg
from dotenv import load_dotenv
from pydantic import BaseModel

# if TYPE_CHECKING:
from src.order_repository import OrderRepository

load_dotenv()
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


class OrderData(BaseModel):
    id_order: str
    cpf: str
    total: float
    freight: float


class OrderRepositoryDatabase(OrderRepository):
    async def save(self, order) -> None:
        async with asyncpg.create_pool(
            database=db_name, host=db_host, port=db_port, user=db_user, password=db_password
        ) as pool:
            async with pool.acquire() as connection:
                await connection.execute(
                    'INSERT INTO ecommerce.order (id_order, cpf, total, freight) VALUES ($1, $2, $3, $4);',
                    order.id_order,
                    order.cpf,
                    order.total,
                    order.freight,
                )
                for item in order.items:
                    await connection.execute(
                        'INSERT INTO ecommerce.item (id_order, id_product, price, quantity) VALUES ($1, $2, $3, $4);',
                        order.id_order,
                        item.id_product,
                        item.price,
                        item.quantity,
                    )

    async def get_by_id(self, id: str) -> OrderData:
        async with asyncpg.create_pool(
            database=db_name, host=db_host, port=db_port, user=db_user, password=db_password
        ) as pool:
            async with pool.acquire() as connection:
                row = await connection.fetchrow(
                    'SELECT * FROM ecommerce.order WHERE id_order = $1;', id
                )
                return OrderData(
                    id_order=row[0],
                    cpf=row[1],
                    total=row[2],
                    freight=row[3],
                )
