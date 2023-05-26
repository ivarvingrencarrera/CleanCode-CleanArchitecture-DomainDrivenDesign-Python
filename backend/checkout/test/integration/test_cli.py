import json

from checkout.src.application.usecase.checkout import Checkout
from checkout.src.infra.cli.cli_controller import CLIController
from checkout.src.infra.cli.cli_handler import CLIHandler
from checkout.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from checkout.src.infra.gateway.currency_gateway_http import CurrencyGatewayHttp
from checkout.src.infra.http.request_adapter import RequestAdapter
from checkout.src.infra.repository.coupon_repository_database import CouponRepositoryDatabase
from checkout.src.infra.repository.order_repository_database import OrderRepositoryDatabase
from checkout.src.infra.repository.product_repository_database import ProductRepositoryDatabase


async def test_cli():
    connection = AsyncPGAdapter()
    http_client = RequestAdapter()
    currency_gateway = CurrencyGatewayHttp(http_client)
    product_repository = ProductRepositoryDatabase(connection)
    coupon_repository = CouponRepositoryDatabase(connection)
    order_repository = OrderRepositoryDatabase(connection)
    checkout = Checkout(currency_gateway, product_repository, coupon_repository, order_repository)
    output = None

    class TestCLIHandler(CLIHandler):
        # def __init__(self):
        def write(self, text):
            nonlocal output
            output = json.loads(text)

    handler = TestCLIHandler()
    CLIController(handler, checkout)
    await handler.type('set-cpf 08704506626')
    await handler.type('add-item 1 1')
    await handler.type('add-item 2 1')
    await handler.type('add-item 3 3')
    await handler.type('checkout')

    assert output['total'] == 6090
    assert output['freight'] == 280
    await connection.disconnect()
