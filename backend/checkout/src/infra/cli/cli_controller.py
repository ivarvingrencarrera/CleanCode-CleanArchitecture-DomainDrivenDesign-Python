import json

from pydantic import BaseModel

from checkout.src.application.usecase.checkout import Checkout
from checkout.src.infra.cli.cli_handler import CLIHandler


class Item(BaseModel):
    id_product: int
    quantity: int


class Input(BaseModel):
    cpf: str
    items: list[Item]
    coupon: str | None = None
    origin: str | None = None
    destination: str | None = None


class CLIController:
    def __init__(self, handler: CLIHandler, checkout: Checkout) -> None:
        self.input_ = Input(cpf='', items=[])
        self.handler = handler
        self.checkout = checkout
        self.handler.on('set-cpf', self.set_cpf)
        self.handler.on('add-item', self.add_item)
        self.handler.on('checkout', self.do_checkout)

    async def set_cpf(self, params):
        self.input_.cpf = params

    async def add_item(self, params):
        id_product, quantity = params.split(' ')
        item = Item(id_product=int(id_product), quantity=int(quantity))
        self.input_.items.append(item)

    async def do_checkout(self, _):
        try:
            output = await self.checkout.execute(self.input_.dict())
            self.handler.write(json.dumps(output))
        except Exception as e:
            self.handler.write(str(e))
