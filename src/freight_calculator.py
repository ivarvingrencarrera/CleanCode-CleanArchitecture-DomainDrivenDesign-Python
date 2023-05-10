from src.product_repository_database import ProductData


class FreightCalculator:
    @staticmethod
    def calculate(product: ProductData) -> float:
        volume = product.width / 100 * product.height / 100 * product.length / 100
        density = product.weight / volume
        return 1000 * volume * (density / 100)
