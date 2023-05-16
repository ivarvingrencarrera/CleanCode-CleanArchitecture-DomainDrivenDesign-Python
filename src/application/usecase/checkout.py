from datetime import datetime

from pydantic import BaseModel

from src.coupon_repository import CouponRepository
from src.coupon_repository_database import CouponRepositoryDatabase
from src.currency_gateway import CurrencyGateway
from src.currency_gateway_http import CurrencyGatewayHttp
from src.domain.entity.currency_table import CurrencyTable
from src.domain.entity.freight_calculator import FreightCalculator
from src.domain.entity.order import Order
from src.domain.entity.product import Product
from src.order_repository import OrderRepository
from src.order_repository_database import OrderRepositoryDatabase
from src.product_repository import ProductRepository
from src.product_repository_database import ProductRepositoryDatabase


class Item(BaseModel):
    id_product: int
    quantity: int
    price: float | None = None
    currency: str | None = None


class Input(BaseModel):
    uuid: str | None = None
    cpf: str
    items: list[Item] | None = None
    coupon: str | None = None
    origin: str | None = None
    destination: str | None = None


class Output(BaseModel):
    total: float
    freight: float


class Checkout:
    def __init__(
        self,
        currency_gateway: CurrencyGateway | None = None,
        product_repository: ProductRepository | None = None,
        coupon_repository: CouponRepository | None = None,
        order_repository: OrderRepository | None = None,
    ):
        self.currency_gateway = currency_gateway or CurrencyGatewayHttp()
        self.product_repository = product_repository or ProductRepositoryDatabase()
        self.coupon_repository = coupon_repository or CouponRepositoryDatabase()
        self.order_repository = order_repository or OrderRepositoryDatabase()

    async def execute(self, input_: Input) -> Output:
        currencies = await self.currency_gateway.get_currencies()
        currency_table = CurrencyTable()
        currency_table.add_currency(currencies.currency, currencies.rates)   # add USD currency
        sequence = await self.order_repository.count()
        order = Order(input_.uuid, input_.cpf, currency_table, sequence, datetime.now())
        freight = 0
        if input_.items:
            for item in input_.items:
                product: Product = await self.product_repository.get_product(item.id_product)
                order.add_item(product, item.quantity)
                item_freight = FreightCalculator.calculate(product)
                freight += max(item_freight, 10) * item.quantity
        if input_.origin and input_.destination:
            order.freight = freight
        if input_.coupon:
            coupon = await self.coupon_repository.get_coupon(input_.coupon)
            order.add_coupon(coupon)
        total = order.get_total()

        await self.order_repository.save(order)
        return Output(total=total, freight=freight)
