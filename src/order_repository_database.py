import os
from datetime import datetime

import asyncpg
from dotenv import load_dotenv
from pydantic import BaseModel

from src.domain.entity.item import Item
from src.domain.entity.order import Order

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
    code: str
    total: float
    freight: float


class ItemData(BaseModel):
    id_product: int
    price: float
    quantity: int
    currency: str


class OrderRepositoryDatabase(OrderRepository):
    async def save(self, order: Order) -> None:
        async with asyncpg.create_pool(
            database=db_name, host=db_host, port=db_port, user=db_user, password=db_password
        ) as pool:
            async with pool.acquire() as connection:
                await connection.execute(
                    'INSERT INTO ecommerce.order (id_order, cpf, code, total, freight)' 'VALUES ($1, $2, $3, $4, $5);',
                    order.id_order,
                    order.cpf,
                    order.code,
                    order.get_total(),
                    order.freight,
                )
                for item in order.items:
                    await connection.execute(
                        'INSERT INTO ecommerce.item (id_order, id_product, price, quantity)' 'VALUES ($1, $2, $3, $4);',
                        order.id_order,
                        item.id_product,
                        item.price,
                        item.quantity,
                    )

    async def get_by_id(self, id_order: str) -> Order:
        async with asyncpg.create_pool(
            database=db_name, host=db_host, port=db_port, user=db_user, password=db_password
        ) as pool:
            async with pool.acquire() as connection:
                order_row = await connection.fetchrow('SELECT * FROM ecommerce.order WHERE id_order = $1;', id_order)
                order_data = OrderData(
                    id_order=order_row[0],
                    cpf=order_row[1],
                    code=order_row[2],
                    total=order_row[3],
                    freight=order_row[3],
                )
                order = Order(order_data.id_order, order_data.cpf, None, 1, datetime.now())
                items = await connection.fetch('SELECT * FROM ecommerce.item WHERE id_order = $1;', id_order)
                items_data = [
                    ItemData(
                        id_product=item['id_product'], price=item['price'], quantity=item['quantity'], currency='BRL'
                    )
                    for item in items
                ]
                for item_data in items_data:
                    order.items.append(
                        Item(item_data.id_product, item_data.price, item_data.quantity, item_data.currency)
                    )
                return order

    async def count(self) -> int:
        async with asyncpg.create_pool(
            database=db_name, host=db_host, port=db_port, user=db_user, password=db_password
        ) as pool:
            async with pool.acquire() as connection:
                row = await connection.fetchrow('SELECT COUNT(*) FROM ecommerce.order;')
                return row[0]
