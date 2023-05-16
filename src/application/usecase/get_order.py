from pydantic import BaseModel

from src.domain.entity.order import Order
from src.order_repository import OrderRepository
from src.order_repository_database import OrderRepositoryDatabase


class Output(BaseModel):
    code: str
    total: float
    freight: float


class GetOrder:
    def __init__(self, order_repository: OrderRepository | None = None) -> None:
        self.order_repository = order_repository or OrderRepositoryDatabase()

    async def execute(self, id_order: str) -> Output:
        order: Order = await self.order_repository.get_by_id(id_order)
        return Output(code=order.get_code(), total=order.get_total(), freight=order.freight)
