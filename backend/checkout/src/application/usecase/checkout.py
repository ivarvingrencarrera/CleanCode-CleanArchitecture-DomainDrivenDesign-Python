from datetime import datetime

from pydantic import BaseModel

from checkout.src.application.gateway.currency_gateway import CurrencyGateway
from checkout.src.application.repository.coupon_repository import CouponRepository
from checkout.src.application.repository.order_repository import OrderRepository
from checkout.src.application.repository.product_repository import ProductRepository
from checkout.src.domain.entity.currency_table import CurrencyTable
from checkout.src.domain.entity.freight_calculator import FreightCalculator
from checkout.src.domain.entity.order import Order
from checkout.src.domain.entity.product import Product


class Item(BaseModel):
    id_product: int
    quantity: int
    price: float | None = None
    currency: str | None = None


class Input(BaseModel):
    uuid: str | None = None
    cpf: str
    items: list[Item]
    coupon: str | None = None
    origin: str | None = None
    destination: str | None = None


class Checkout:
    def __init__(
        self,
        currency_gateway: CurrencyGateway,
        product_repository: ProductRepository,
        coupon_repository: CouponRepository,
        order_repository: OrderRepository,
    ):
        self.currency_gateway = currency_gateway
        self.product_repository = product_repository
        self.coupon_repository = coupon_repository
        self.order_repository = order_repository

    async def execute(self, input_data: dict) -> dict:
        input_ = Input(**input_data)
        currencies = await self.currency_gateway.get_currencies()
        currency_table = CurrencyTable()
        currency_table.add_currency(currencies['currency'], currencies['rates'])   # add USD currency
        sequence = await self.order_repository.count()
        order = Order(input_.uuid, input_.cpf, currency_table, sequence, datetime.now())
        freight = 0
        if input_.items:
            for item in input_.items:
                product: Product = await self.product_repository.get_product(item.id_product)
                order.add_item(product, item.quantity)
                item_freight = FreightCalculator.calculate(product, item.quantity)
                freight += item_freight
        if input_.origin and input_.destination:
            order.freight = freight
        if input_.coupon:
            coupon = await self.coupon_repository.get_coupon(input_.coupon)
            order.add_coupon(coupon)
        total = order.get_total()

        await self.order_repository.save(order)
        return {'total': total, 'freight': freight}
