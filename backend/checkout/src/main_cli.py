import asyncio
import sys
from pathlib import Path

projeto_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(projeto_dir))

from checkout.src.application.usecase.checkout import Checkout
from checkout.src.infra.cli.cli_controller import CLIController
from checkout.src.infra.cli.cli_handler_python import CLIHandlerPython
from checkout.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from checkout.src.infra.gateway.currency_gateway_http import CurrencyGatewayHttp
from checkout.src.infra.http.axios_adapter import RequestAdapter
from checkout.src.infra.repository.coupon_repository_database import CouponRepositoryDatabase
from checkout.src.infra.repository.order_repository_database import OrderRepositoryDatabase
from checkout.src.infra.repository.product_repository_database import ProductRepositoryDatabase


async def run_cli():
    connection = AsyncPGAdapter()
    http_client = RequestAdapter()
    currency_gateway = CurrencyGatewayHttp(http_client)
    product_repository = ProductRepositoryDatabase(connection)
    coupon_repository = CouponRepositoryDatabase(connection)
    order_repository = OrderRepositoryDatabase(connection)
    checkout = Checkout(currency_gateway, product_repository, coupon_repository, order_repository)
    handler = CLIHandlerPython()

    CLIController(handler, checkout)
    await handler.read_input()

    await connection.disconnect()


if __name__ == '__main__':
    asyncio.run(run_cli())
