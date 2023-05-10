import os

from dotenv import load_dotenv
from pydantic import BaseModel

from src.order_repository import OrderRepository
from src.order_repository_database import OrderData, OrderRepositoryDatabase

load_dotenv()
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


class Output(BaseModel):
    total: float
    freight: float


class GetOrder:
    def __init__(self, order_repository=None) -> None:
        self.order_repository: OrderRepository = order_repository or OrderRepositoryDatabase()

    async def execute(self, id: str) -> Output:
        output = Output(total=0, freight=0)
        order_data: OrderData = await self.order_repository.get_by_id(id)
        output.total = order_data.total
        output.freight = order_data.freight
        return output
