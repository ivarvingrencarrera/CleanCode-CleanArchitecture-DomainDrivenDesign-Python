from pydantic import BaseModel

from checkout.src.application.repository.order_repository import OrderRepository
from checkout.src.domain.entity.order import Order


class Output(BaseModel):
    code: str
    total: float
    freight: float


class GetOrder:
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    async def execute(self, id_order: str) -> Output:
        order: Order = await self.order_repository.get_by_id(id_order)
        return Output(code=order.get_code(), total=order.get_total(), freight=order.freight)
