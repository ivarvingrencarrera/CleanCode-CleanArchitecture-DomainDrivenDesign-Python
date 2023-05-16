from src.domain.entity.product import Product


class FreightCalculator:
    @staticmethod
    def calculate(product: Product) -> float:
        volume = product.get_volume()
        density = product.weight / volume
        return 1000 * volume * (density / 100)
