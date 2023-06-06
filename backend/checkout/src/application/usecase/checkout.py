from datetime import datetime
from checkout.src.application.gateway.stock_gateway import StockGateway
from checkout.src.infra.gateway.stock_gateway_http import StockGatewayHttp
from checkout.src.application.usecase.usecase import UseCase
from checkout.src.infra.gateway.auth_gateway_http import AuthGatewayHttp
from checkout.src.application.gateway.auth_gateway import AuthGateway
from checkout.src.application.gateway.catalog_gateway import CatalogGateway
from checkout.src.application.gateway.currency_gateway import CurrencyGateway
from checkout.src.application.gateway.freight_gateway import FreightGateway
from checkout.src.application.gateway.freight_gateway import Input as FreightInput
from checkout.src.application.gateway.freight_gateway import Item as FreightItem
from checkout.src.application.repository.coupon_repository import CouponRepository
from checkout.src.application.repository.order_repository import OrderRepository
from checkout.src.application.repository.product_repository import ProductRepository
from checkout.src.domain.entity.currency_table import CurrencyTable
from checkout.src.domain.entity.order import Order
from checkout.src.domain.entity.product import Product
from checkout.src.infra.gateway.catalog_gateway_http import CatalogGatewayHttp
from checkout.src.infra.gateway.freight_gateway_http import FreightGatewayHttp
from checkout.src.infra.http.requests_adapter import RequestsAdapter
from pydantic import BaseModel


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


class Checkout(UseCase):
    def __init__(
        self,
        currency_gateway: CurrencyGateway,
        product_repository: ProductRepository,
        coupon_repository: CouponRepository,
        order_repository: OrderRepository,
        freight_gateway: FreightGateway = FreightGatewayHttp(RequestsAdapter()),
        catalog_gateway: CatalogGateway = CatalogGatewayHttp(RequestsAdapter()),
        stock_gateway: StockGateway = StockGatewayHttp(RequestsAdapter()),
    ):
        self.currency_gateway = currency_gateway
        self.product_repository = product_repository
        self.coupon_repository = coupon_repository
        self.order_repository = order_repository
        self.freight_gateway = freight_gateway
        self.catalog_gateway = catalog_gateway
        self.stock_gateway = stock_gateway

    async def execute(self, input_data: dict) -> dict:
        input_ = Input(**input_data)
        currencies = await self.currency_gateway.get_currencies()
        currency_table = CurrencyTable()
        currency_table.add_currency(currencies['currency'], currencies['rates'])   # add USD currency
        sequence = await self.order_repository.count()
        order = Order(input_.uuid, input_.cpf, currency_table, sequence, datetime.now())
        freight_input = FreightInput(items=[], origin=input_.origin, destination=input_.destination)
        if input_.items:
            for item in input_.items:
                product: Product = await self.catalog_gateway.get_product(item.id_product)
                order.add_item(product, item.quantity)
                freight_input.items.append(
                    FreightItem(
                        width=product.width,
                        height=product.height,
                        length=product.length,
                        weight=product.weight,
                        quantity=item.quantity,
                    )
                )
        freight_output = await self.freight_gateway.calculate_freight(freight_input)
        freight = freight_output.freight
        if input_.origin and input_.destination:
            order.freight = freight
        if input_.coupon:
            coupon = await self.coupon_repository.get_coupon(input_.coupon)
            order.add_coupon(coupon)
        total = order.get_total()

        await self.order_repository.save(order)
        await self.stock_gateway.decrement_stock(input_)
        return {'total': total, 'freight': freight}
