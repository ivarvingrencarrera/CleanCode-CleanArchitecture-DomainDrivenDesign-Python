import os
from datetime import datetime

from dotenv import load_dotenv
from pydantic import BaseModel

from src.coupon_repository import CouponRepository
from src.coupon_repository_database import CouponRepositoryDatabase
from src.cpf import CPF
from src.currency_gateway_http import CurrencyGatewayHttp
from src.freight_calculator import FreightCalculator
from src.product_repository import ProductRepository
from src.product_repository_database import ProductData, ProductRepositoryDatabase

load_dotenv()
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


class Item(BaseModel):
    id_product: int
    quantity: int


class Input(BaseModel):
    cpf: str
    items: list[Item] | None = None
    coupon: str | None = None
    origin: str | None = None
    destination: str | None = None


class Output(BaseModel):
    total: float
    freight: float


class CouponData(BaseModel):
    code: str
    percentage: float
    expire_date: datetime


class Checkout:
    def __init__(self) -> None:
        self.product_repository: ProductRepository = ProductRepositoryDatabase()
        self.coupon_repository: CouponRepository = CouponRepositoryDatabase()

    async def execute(self, input_: Input):
        cpf = CPF(input_.cpf)
        output = Output(total=0, freight=0)
        currency_gateway = CurrencyGatewayHttp()
        currencies = await currency_gateway.get_currencies()
        if not cpf.is_valid():
            raise ValueError('Invalid cpf')
        if input_.items:
            items = []
            for item in input_.items:
                if item.quantity <= 0:
                    raise ValueError('Invalid quantity')
                if item.id_product in items:
                    raise ValueError('Duplicated item')
                product_data: ProductData = await self.product_repository.get_product(
                    item.id_product
                )
                if (
                    product_data.height <= 0
                    or product_data.length <= 0
                    or product_data.weight <= 0
                    or product_data.width <= 0
                ):
                    raise ValueError('Invalid dimension')
                if product_data.currency == 'USD':
                    output.total += product_data.price * item.quantity * currencies['usd']
                else:
                    output.total += product_data.price * item.quantity
                item_freight = FreightCalculator.calculate(product_data)
                output.freight += max(item_freight, 10) * item.quantity
                items.append(item.id_product)
        if input_.coupon:
            coupon_data = await self.coupon_repository.get_coupon(input_.coupon)
            if coupon_data.expire_date > datetime.now():
                output.total -= (output.total * coupon_data.percentage) / 100
        if input_.origin and input_.destination:
            output.total += output.freight
        return output
