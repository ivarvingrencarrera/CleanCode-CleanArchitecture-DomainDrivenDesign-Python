import pytest

from src.checkout import Checkout, Input, Item

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
    assert output.total == 6090


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
    assert output.total == 4872


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
    assert output.total == 6090


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
    assert output.total == 3090
    assert output.freight == 90


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
    assert output.total == 40
    assert output.freight == 10

async def test_checkout_with_dollar_product() -> None:
    input_ = Input(
        cpf='353.775.320-90',
        items=[Item(id_product=5, quantity=1)],
    )
    output = await checkout.execute(input_)
    assert output.total == 3000

