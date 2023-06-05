class FreightCalculator:
    @staticmethod
    def calculate(  # noqa: PLR0913
        distance: float, width: int, height: int, length: int, weight: float, quantity: int = 1
    ) -> float:
        volume = width / 100 * height / 100 * length / 100
        density = weight / volume
        item_freight = distance * volume * (density / 100)
        return max(item_freight, 10) * quantity
