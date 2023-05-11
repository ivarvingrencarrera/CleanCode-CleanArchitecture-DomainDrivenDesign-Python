from src.validate_coupon import ValidateCoupon

validate_coupon = ValidateCoupon()

async def test_checkout_with_valid_coupon() -> None:
    input_ = 'VALE20'
    output = await validate_coupon.execute(input_)
    assert output == True

async def test_checkout_with_invalid_coupon() -> None:
    input_ = 'VALE10'
    output = await validate_coupon.execute(input_)
    assert output == False
