class StockEntry:
    def __init__(self, id_product: int, operation: str, quantity: int) -> None:
        if operation not in ('in', 'out'):
            raise ValueError('Invalid operation')
        if quantity <= 0:
            raise ValueError('Invalid quantity')
        self.id_product = id_product
        self.operation = operation
        self.quantity = quantity