from checkout.src.application.gateway.freight_gateway import FreightGateway
from checkout.src.application.gateway.freight_gateway import Input as FreightInput
from checkout.src.application.gateway.freight_gateway import Item as FreightItem
from checkout.src.application.repository.product_repository import ProductRepository
from checkout.src.domain.entity.product import Product
from checkout.src.infra.gateway.freight_gateway_http import FreightGatewayHttp
from checkout.src.infra.http.requests_adapter import RequestsAdapter
from pydantic import BaseModel


class Input(BaseModel):
    items: list


class Output(BaseModel):
    freight: float


class SimulateFreight:
    def __init__(
        self,
        product_repository: ProductRepository,
        freight_gateway: FreightGateway = FreightGatewayHttp(RequestsAdapter()),
    ) -> None:
        self.product_repository = product_repository
        self.freight_gateway = freight_gateway

    async def execute(self, input_: Input) -> Output:
        output = Output(freight=0)
        freight_input = FreightInput(items=[])
        if input_.items:
            for item in input_.items:
                product: Product = await self.product_repository.get_product(item.id_product)
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
        output.freight = freight_output.freight
        return output
