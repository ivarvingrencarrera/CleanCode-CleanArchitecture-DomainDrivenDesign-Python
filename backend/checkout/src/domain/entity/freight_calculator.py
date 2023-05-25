from checkout.src.domain.entity.product import Product


class FreightCalculator:
    @staticmethod
    def calculate(product: Product, quantity: int = 1) -> int:
        volume = product.get_volume()
        density = product.weight / volume
        item_freight = 1000 * volume * (density / 100)
        return max(item_freight, 10) * quantity
