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
    item1 = Item(id_product=1, quantity=1)
    item2 = Item(id_product=2, quantity=1)
    item3 = Item(id_product=3, quantity=3)
    input_ = Input(cpf='353.775.320-90', items=[item1, item2, item3])
    output = await checkout.execute(input_)
    total = 6090
    assert output.total == total


async def test_checkout_with_3_products_with_coupon() -> None:
    item1 = Item(id_product=1, quantity=1)
    item2 = Item(id_product=2, quantity=1)
    item3 = Item(id_product=3, quantity=3)
    input_ = Input(cpf='353.775.320-90', items=[item1, item2, item3], coupon='VALE20')
    output = await checkout.execute(input_)
    total = 4872
    assert output.total == total


async def test_checkout_with_3_products_with_invalid_coupon() -> None:
    item1 = Item(id_product=1, quantity=1)
    item2 = Item(id_product=2, quantity=1)
    item3 = Item(id_product=3, quantity=3)
    input_ = Input(cpf='353.775.320-90', items=[item1, item2, item3], coupon='VALE10')
    output = await checkout.execute(input_)
    total = 6090
    assert output.total == total


async def test_checkout_with_negative_quantity() -> None:
    item = Item(id_product=1, quantity=-1)
    input_ = Input(cpf='353.775.320-90', items=[item])
    with pytest.raises(ValueError, match='Invalid quantity'):
        await checkout.execute(input_)


async def test_checkout_with_duplicated_item() -> None:
    item1 = Item(id_product=1, quantity=1)
    item2 = Item(id_product=1, quantity=1)
    input_ = Input(cpf='353.775.320-90', items=[item1, item2])
    with pytest.raises(ValueError, match='Duplicated item'):
        await checkout.execute(input_)


async def test_checkout_with_1_product_calculating_freight() -> None:
    item = Item(id_product=1, quantity=3)
    input_ = Input(cpf='353.775.320-90', items=[item], origin='22060030', destination='88015600')
    output = await checkout.execute(input_)
    total = 3090
    assert output.total == total
    freight = 90
    assert output.freight == freight


async def test_checkout_with_invalid_dimension() -> None:
    item = Item(id_product=4, quantity=1)
    input_ = Input(cpf='353.775.320-90', items=[item])
    with pytest.raises(ValueError, match='Invalid dimension'):
        await checkout.execute(input_)


async def test_checkout_with_1_product_calculating_minimum_freight() -> None:
    item = Item(id_product=3, quantity=1)
    input_ = Input(cpf='353.775.320-90', items=[item], origin='22060030', destination='88015600')
    output = await checkout.execute(input_)
    total = 40
    assert output.total == total
    freight = 10
    assert output.freight == freight
