import uuid
from datetime import datetime

from src.domain.entity.coupon import Coupon
from src.domain.entity.cpf import CPF
from src.domain.entity.currency_table import CurrencyTable
from src.domain.entity.item import Item
from src.domain.entity.product import Product


class Order:
    def __init__(
        self,
        id_order: str,
        cpf: str,
        currency_table: CurrencyTable | None = None,
        sequence: int | None = None,
        date: datetime | None = None,
    ) -> None:
        self.id_order = id_order or uuid.uuid4().hex
        self.cpf = CPF(cpf).value
        self.currency_table = currency_table or CurrencyTable()
        self.sequence = sequence or 1
        self.date = date or datetime.now()
        self.items: list[Item] = []
        self.code = f'{self.date.year}{str(self.sequence).zfill(8)}'
        self.freight: float = 0
        self.coupon: Coupon = None

    def add_item(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Invalid quantity')
        if any(item.id_product == product.id_product for item in self.items):
            raise ValueError('Duplicated item')
        self.items.append(
            Item(id_product=product.id_product, price=product.price, quantity=quantity, currency=product.currency)
        )

    def add_coupon(self, coupon: Coupon) -> None:
        if not coupon.is_expired(self.date):
            self.coupon = coupon

    def get_total(self) -> float:
        total = sum(item.price * item.quantity * self.currency_table.get_currency(item.currency) for item in self.items)
        if self.coupon:
            total -= self.coupon.calculate_discount(total)

        total += self.freight
        return total

    def get_code(self) -> str:
        return self.code
