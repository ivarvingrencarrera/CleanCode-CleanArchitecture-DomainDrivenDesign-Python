from pydantic import BaseModel

from checkout import Checkout


class Item(BaseModel):
    id_product: int
    quantity: int


class Input(BaseModel):
    cpf: str
    items: list[Item]


input_data = Input(cpf='', items=[])

while True:
    command = input().strip()
    if command.startswith('set-cpf'):
        input_data.cpf = command.replace('set-cpf ', '')
    elif command.startswith('add-item'):
        id_product, quantity = map(int, command.replace('add-item ', '', 1).split())
        item = Item(id_product=id_product, quantity=quantity)
        input_data.items.append(item)
    elif command.startswith('checkout'):
        try:
            checkout = Checkout()
            output = checkout.execute(input_data)
            print(output)
        except Exception as e:
            print(e.message)
