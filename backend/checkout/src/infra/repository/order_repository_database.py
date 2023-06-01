from checkout.src.application.repository.order_repository import OrderRepository
from checkout.src.domain.entity.item import Item
from checkout.src.domain.entity.order import Order
from checkout.src.infra.database.connection import Connection


class OrderRepositoryDatabase(OrderRepository):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def save(self, order: Order) -> None:
        order_query = 'INSERT INTO ecommerce.order (id_order, cpf, code, total, freight)' 'VALUES ($1, $2, $3, $4, $5);'
        order_data = (order.id_order, order.cpf, order.code, order.get_total(), order.freight)
        await self.connection.insert(order_query, *order_data)
        query_item = 'INSERT INTO ecommerce.item (id_order, id_product, price, quantity)' 'VALUES ($1, $2, $3, $4);'
        for item in order.items:
            item_data = (order.id_order, item.id_product, item.price, item.quantity)
            await self.connection.insert(query_item, *item_data)

    async def get_by_id(self, id_order: str) -> Order:
        order_query = 'SELECT * FROM ecommerce.order WHERE id_order = $1;'
        order_data = await self.connection.select(order_query, id_order)
        order_row = order_data[0]
        order = Order(order_row.id_order, order_row.cpf)
        items_query = 'SELECT * FROM ecommerce.item WHERE id_order = $1;'
        items_data = await self.connection.select(items_query, id_order)
        for item_data in items_data:
            order.items.append(Item(item_data.id_product, float(item_data.price), item_data.quantity, 'BRL'))
        return order

    async def count(self) -> int:
        order_row = await self.connection.select('SELECT COUNT(*) FROM ecommerce.order;')
        return order_row.count
