class Item:
    def __init__(self, id_product: int, quantity: int, price: float, currency: str) -> None:
        self.id_product = id_product
        self.price = price
        self.quantity = quantity
        self.currency = currency or 'BRL'
