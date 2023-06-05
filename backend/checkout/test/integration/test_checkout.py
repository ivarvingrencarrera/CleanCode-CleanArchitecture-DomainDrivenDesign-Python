import json
import uuid
from datetime import datetime
from unittest import mock
from unittest.mock import AsyncMock, patch
from checkout.src.infra.gateway.catalog_gateway_http import CatalogGatewayHttp

import pytest
from checkout.src.application.usecase.checkout import Checkout
from checkout.src.application.usecase.get_order import GetOrder
from checkout.src.domain.entity.coupon import Coupon
from checkout.src.domain.entity.product import Product
from checkout.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from checkout.src.infra.gateway.currency_gateway_http import CurrencyGatewayHttp
from checkout.src.infra.http.requests_adapter import RequestsAdapter
from checkout.src.infra.repository.coupon_repository_database import (
    CouponRepositoryDatabase,
)
from checkout.src.infra.repository.order_repository_database import (
    OrderRepositoryDatabase,
)
from checkout.src.infra.repository.product_repository_database import (
    ProductRepositoryDatabase,
)

connection = AsyncPGAdapter()
http_client = RequestsAdapter()
currency_gateway = CurrencyGatewayHttp(http_client)
product_repository = ProductRepositoryDatabase(connection)
coupon_repository = CouponRepositoryDatabase(connection)
order_repository = OrderRepositoryDatabase(connection)
checkout = Checkout(currency_gateway, product_repository, coupon_repository, order_repository)
get_order = GetOrder(order_repository)


async def test_checkout_with_invalid_cpf() -> None:
    input_ = {'cpf': '406.302.170-27', 'items': []}
    with pytest.raises(ValueError, match='Invalid cpf'):
        await checkout.execute(input_)


async def test_empty_checkout() -> None:
    input_ = {'cpf': '353.775.320-90', 'items': []}
    output = await checkout.execute(input_)
    assert output['total'] == 0


async def test_checkout_with_3_products() -> None:
    uuid_ = uuid.uuid4().hex
    input_ = {
        'uuid': uuid_,
        'cpf': '353.775.320-90',
        'items': [{'id_product': 1, 'quantity': 1}, {'id_product': 2, 'quantity': 1}, {'id_product': 3, 'quantity': 3}],
    }
    await checkout.execute(input_)
    output = await get_order.execute(uuid_)
    total = 6090
    assert output.total == total


async def test_checkout_with_3_products_with_coupon() -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [{'id_product': 1, 'quantity': 1}, {'id_product': 2, 'quantity': 1}, {'id_product': 3, 'quantity': 3}],
        'coupon': 'VALE20',
    }
    output = await checkout.execute(input_)
    total = 4872
    assert output['total'] == total


async def test_checkout_with_3_products_with_invalid_coupon() -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [{'id_product': 1, 'quantity': 1}, {'id_product': 2, 'quantity': 1}, {'id_product': 3, 'quantity': 3}],
        'coupon': 'VALE10',
    }
    output = await checkout.execute(input_)
    total = 6090
    assert output['total'] == total


async def test_checkout_with_negative_quantity() -> None:
    input_ = {'cpf': '353.775.320-90', 'items': [{'id_product': 1, 'quantity': -1}]}
    with pytest.raises(ValueError, match='Invalid quantity'):
        await checkout.execute(input_)


async def test_checkout_with_duplicated_item() -> None:
    input_ = {'cpf': '353.775.320-90', 'items': [{'id_product': 1, 'quantity': 1}, {'id_product': 1, 'quantity': 1}]}
    with pytest.raises(ValueError, match='Duplicated item'):
        await checkout.execute(input_)


async def test_checkout_with_1_product_calculating_freight() -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [{'id_product': 1, 'quantity': 1}],
        'origin': 22060030,
        'destination': 88015600,
    }
    output = await checkout.execute(input_)
    total = 1022.4466533402449
    assert output['total'] == total
    freight = 22.446653340244893
    assert output['freight'] == freight


async def test_checkout_with_invalid_dimension() -> None:
    input_ = {'cpf': '353.775.320-90', 'items': [{'id_product': 4, 'quantity': 1}]}
    with pytest.raises(ValueError, match='Invalid dimension'):
        await checkout.execute(input_)


async def test_checkout_with_1_product_calculating_minimum_freight() -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [{'id_product': 3, 'quantity': 1}],
        'origin': 22060030,
        'destination': 88015600,
    }
    output = await checkout.execute(input_)
    total = 40
    assert output['total'] == total
    freight = 10
    assert output['freight'] == freight


async def test_checkout_with_one_product_in_dollar_using_stub() -> None:
    with patch.object(
        CurrencyGatewayHttp,
        'get_currencies',
        new_callable=AsyncMock,
        return_value={'currency': 'USD', 'symbol': '$', 'name': 'United States dollar', 'rates': 4},
    ), patch.object(
        ProductRepositoryDatabase,
        'get_product',
        new_callable=AsyncMock,
        return_value=Product(6, 'A', 1000, 100, 30, 10, 3, 'USD'),
    ):
        input_ = {'cpf': '353.775.320-90', 'items': [{'id_product': 5, 'quantity': 1}]}
        output = await checkout.execute(input_)
        total = 4000
        assert output['total'] == total


async def test_create_order_with_discount_coupon_using_spy() -> None:
    expire_date: datetime = datetime.strptime('2023-10-01 10:00:00', '%Y-%m-%d %H:%M:%S')
    with mock.patch.object(CouponRepositoryDatabase, 'get_coupon') as coupon_repository_spy:
        coupon_repository_spy.return_value = Coupon(code='VALE20', percentage=20, expire_date=expire_date)
        input_data = {
            'cpf': '407.302.170-27',
            'items': [
                {'id_product': 1, 'quantity': 1},
                {'id_product': 2, 'quantity': 1},
                {'id_product': 3, 'quantity': 3},
            ],
            'coupon': 'VALE20',
        }
        output = await checkout.execute(input_data)
        total = 4872
        assert output['total'] == total
        coupon_repository_spy.assert_called_once_with('VALE20')
        coupon_repository_spy.assert_called_once()


@patch.object(
    CurrencyGatewayHttp,
    'get_currencies',
    new_callable=AsyncMock,
    return_value={'currency': 'USD', 'symbol': '$', 'name': 'United States dollar', 'rates': 3},
)
async def test_checkout_with_one_product_in_dollar_using_mock(
    currency_gateway_mock: CurrencyGatewayHttp,
) -> None:
    input_ = {'cpf': '353.775.320-90', 'items': [{'id_product': 5, 'quantity': 1}]}
    output = await checkout.execute(input_)
    total = 3000
    assert output['total'] == total
    currency_gateway_mock.assert_called_once()


async def test_checkout_with_one_product_in_dollar_using_fake() -> None:
    class CurrencyGatewayFake:
        async def get_currencies(self) -> json:
            return {'currency': 'USD', 'symbol': '$', 'name': 'United States dollar', 'rates': 5}

    class ProductRepositoryFake:
        async def get_product(self, id_product: int) -> Product:
            return Product(6, 'A', 1000, 100, 30, 10, 3, 'USD')
        
    with patch.object(
        CatalogGatewayHttp,
        'get_product',
        new_callable=AsyncMock,
        return_value=Product(6, 'A', 1000, 100, 30, 10, 3, 'USD'),
    ):
        checkout = Checkout(CurrencyGatewayFake(), ProductRepositoryFake(), coupon_repository, order_repository)
        input_ = {'cpf': '353.775.320-90', 'items': [{'id_product': 6, 'quantity': 1}]}
        output = await checkout.execute(input_)
        total = 5000
        assert output['total'] == total


@patch.object(OrderRepositoryDatabase(connection), 'count', new_callable=AsyncMock, return_value=1)
async def test_checkout_and_verify_serial_code(count) -> None:
    uuid_ = uuid.uuid4().hex
    input_ = {
        'uuid': uuid_,
        'cpf': '353.775.320-90',
        'items': [{'id_product': 1, 'quantity': 1}, {'id_product': 2, 'quantity': 1}, {'id_product': 3, 'quantity': 3}],
    }
    await checkout.execute(input_)
    output = await get_order.execute(uuid_)
    code = '202300000001'
    assert output.code == code

async def test_checkout_with_3_products_with_coupon_only_authenticate() -> None:
    input_ = {
        'cpf': '353.775.320-90',
        'items': [{'id_product': 1, 'quantity': 1}, {'id_product': 2, 'quantity': 1}, {'id_product': 3, 'quantity': 3}],
        'coupon': 'VALE20',
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImpvYW9AZ21haWwuY29tIiwiaWF0IjoxNjg2MDAwOTY4LCJleHAiOjE2ODcwMDA5Njh9.BqOVYPYLZpRPSHK4LjvXGzrl0Q8oWesJDv7jrzNT7iw'
    }
    output = await checkout.execute(input_)
    total = 4872
    assert output['total'] == total
