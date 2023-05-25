from checkout.src.application.usecase.validate_coupon import ValidateCoupon
from checkout.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from checkout.src.infra.repository.coupon_repository_database import CouponRepositoryDatabase

connection = AsyncPGAdapter()
coupon_repository = CouponRepositoryDatabase(connection)
validate_coupon = ValidateCoupon(coupon_repository)


async def test_checkout_with_valid_coupon() -> None:
    input_ = 'VALE20'
    output = await validate_coupon.execute(input_)
    assert output is True


async def test_checkout_with_invalid_coupon() -> None:
    input_ = 'VALE10'
    output = await validate_coupon.execute(input_)
    assert output is False
