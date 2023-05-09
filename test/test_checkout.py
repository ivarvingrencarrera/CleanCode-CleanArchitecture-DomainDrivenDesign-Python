import json
from unittest import mock
from unittest.mock import AsyncMock, patch

import pytest

from src.checkout import Checkout, CouponData, Input, Item
from src.coupon_repository_database import CouponRepositoryDatabase
from src.currency_gateway_http import CurrencyGatewayHttp
from src.product_repository_database import ProductData, ProductRepositoryDatabase

checkout = Checkout()


async def test_checkout_with_invalid_cpf() -> None:
    input_ = Input(cpf='406.302.170-27', items=[])
    with pytest.raises(ValueError, match='Invalid cpf'):
        await checkout.execute(input_)


async def test_empty_checkout() -> None:
    input_ = Input(cpf='353.775.320-90', items=[])
    output = await checkout.execute(input_)
    assert output.total == 0


async def test_checkout_with_3_products() -> None:
    input_ = Input(
        cpf='353.775.320-90',
        items=[
            Item(id_product=1, quantity=1),
            Item(id_product=2, quantity=1),
            Item(id_product=3, quantity=3),
        ],
    )
    output = await checkout.execute(input_)
    total = 6090
    assert output.total == total


async def test_checkout_with_3_products_with_coupon() -> None:
    input_ = Input(
        cpf='353.775.320-90',
        items=[
            Item(id_product=1, quantity=1),
            Item(id_product=2, quantity=1),
            Item(id_product=3, quantity=3),
        ],
        coupon='VALE20',
    )
    output = await checkout.execute(input_)
    total = 4872
    assert output.total == total


async def test_checkout_with_3_products_with_invalid_coupon() -> None:
    input_ = Input(
        cpf='353.775.320-90',
        items=[
            Item(id_product=1, quantity=1),
            Item(id_product=2, quantity=1),
            Item(id_product=3, quantity=3),
        ],
        coupon='VALE10',
    )
    output = await checkout.execute(input_)
    total = 6090
    assert output.total == total


async def test_checkout_with_negative_quantity() -> None:
    input_ = Input(cpf='353.775.320-90', items=[Item(id_product=1, quantity=-1)])
    with pytest.raises(ValueError, match='Invalid quantity'):
        await checkout.execute(input_)


async def test_checkout_with_duplicated_item() -> None:
    input_ = Input(
        cpf='353.775.320-90', items=[Item(id_product=1, quantity=1), Item(id_product=1, quantity=1)]
    )
    with pytest.raises(ValueError, match='Duplicated item'):
        await checkout.execute(input_)


async def test_checkout_with_1_product_calculating_freight() -> None:
    input_ = Input(
        cpf='353.775.320-90',
        items=[Item(id_product=1, quantity=3)],
        origin='22060030',
        destination='88015600',
    )
    output = await checkout.execute(input_)
    total = 3090
    assert output.total == total
    freight = 90
    assert output.freight == freight


async def test_checkout_with_invalid_dimension() -> None:
    input_ = Input(cpf='353.775.320-90', items=[Item(id_product=4, quantity=1)])
    with pytest.raises(ValueError, match='Invalid dimension'):
        await checkout.execute(input_)


async def test_checkout_with_1_product_calculating_minimum_freight() -> None:
    input_ = Input(
        cpf='353.775.320-90',
        items=[Item(id_product=3, quantity=1)],
        origin='22060030',
        destination='88015600',
    )
    output = await checkout.execute(input_)
    total = 40
    assert output.total == total
    freight = 10
    assert output.freight == freight


async def test_checkout_with_one_product_in_dollar_using_stub() -> None:
    with patch.object(
        CurrencyGatewayHttp, 'get_currencies', new_callable=AsyncMock, return_value={'usd': 4}
    ), patch.object(
        ProductRepositoryDatabase,
        'get_product',
        new_callable=AsyncMock,
        return_value=ProductData(
            id_product=6,
            description='A',
            price=1000,
            width=100,
            height=30,
            length=10,
            weight=3,
            currency='USD',
        ),
    ):
        input_ = Input(cpf='353.775.320-90', items=[Item(id_product=5, quantity=1)])
        output = await checkout.execute(input_)
        total = 4000
        assert output.total == total

async def test_create_order_with_discount_coupon_using_spy() -> None:
    with mock.patch.object(CouponRepositoryDatabase, 'get_coupon') as coupon_repository_spy:
        coupon_repository_spy.return_value = CouponData(
            code='VALE20', percentage=20, expire_date='2023-10-01T10:00:00'
        )
        input_data = Input(
            cpf='407.302.170-27',
            items=[
                Item(id_product=1, quantity=1),
                Item(id_product=2, quantity=1),
                Item(id_product=3, quantity=3),
            ],
            coupon='VALE20',
        )
        output = await checkout.execute(input_data)
        total = 4872
        assert output.total == total
        coupon_repository_spy.assert_called_once_with('VALE20')
        coupon_repository_spy.assert_called_once()

@patch.object(
    CurrencyGatewayHttp, 'get_currencies', new_callable=AsyncMock, return_value={'usd': 3}
)
async def test_checkout_with_one_product_in_dollar_using_mock(
    currency_gateway_mock: CurrencyGatewayHttp,
) -> None:
    input_ = Input(cpf='353.775.320-90', items=[Item(id_product=5, quantity=1)])
    output = await checkout.execute(input_)
    total = 3000
    assert output.total == total
    currency_gateway_mock.assert_called_once()

async def test_checkout_with_one_product_in_dollar_using_fake() -> None:
    class CurrencyGatewayFake:
        async def get_currencies(self) -> json:
            return {'usd': 4}

    class ProductRepositoryFake:
        async def get_product(self, id_product: int) -> ProductData:
            return ProductData(
                id_product=6,
                description='A',
                price=1000,
                width=100,
                height=30,
                length=10,
                weight=3,
                currency='USD',
            )

    checkout = Checkout(CurrencyGatewayFake(), ProductRepositoryFake())
    input_ = Input(cpf='353.775.320-90', items=[Item(id_product=6, quantity=1)])
    output = await checkout.execute(input_)
    total = 4000
    assert output.total == total