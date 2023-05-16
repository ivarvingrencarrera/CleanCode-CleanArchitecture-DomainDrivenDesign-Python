class CurrencyTable:
    def __init__(self) -> None:
        self.value = {'BRL': 1.0}

    def add_currency(self, currency: str, value: float) -> None:
        self.value[currency] = value

    def get_currency(self, currency: str) -> dict:
        return self.value[currency]
