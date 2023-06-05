from freight.src.application.repository.zip_code_repository import ZIPCodeRepository
from freight.src.application.usecase.calculate_freight import CalculateFreight, Input, Item
from freight.src.domain.entity.zip_code import ZIPCode
from freight.src.infra.http.fast_api_adapter import jsonable_encoder

zip_code_repository = ZIPCodeRepository()


async def simulate_database(code):
    if code == '22060030':
        return ZIPCode('22060030', -27.5945, -48.5477)
    if code == '88015600':
        return ZIPCode('88015600', -22.9129, -43.2003)
    return None


zip_code_repository.get = simulate_database
calculate_freight = CalculateFreight(zip_code_repository)


async def test_calculate_freight_without_origin_and_destination_zipcodes() -> None:
    input_ = Input(
        items=[Item(width=100, height=100, length=100, weight=3, quantity=3)],
    )
    input_json = jsonable_encoder(input_)
    output = await calculate_freight.execute(input_json)
    freight = 90
    assert output['freight'] == freight


async def test_calculate_freight_with_origin_and_destination_zipcodes() -> None:
    input_ = Input(
        items=[Item(width=100, height=100, length=100, weight=3, quantity=1)],
        origin='22060030',
        destination='88015600',
    )
    input_json = jsonable_encoder(input_)
    output = await calculate_freight.execute(input_json)
    freight = 22.446653340244893
    assert output['freight'] == freight
