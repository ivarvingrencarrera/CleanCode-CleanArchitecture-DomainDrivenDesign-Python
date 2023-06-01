class Product:
    def __init__(
        self,
        id_product: int,
        description: str,
        price: float,
        width: int,
        height: int,
        length: int,
        weight: float,
        currency: str,
        volume: float = None,
        density: float = None,
    ) -> None:
        self._validate_dimensions(height, length, weight, width)
        self.id_product = id_product
        self.description = description
        self.price = price
        self.width = width
        self.height = height
        self.length = length
        self.weight = weight
        self.currency = currency
        self.volume = volume
        self.density = density

    @staticmethod
    def _validate_dimensions(*dimensions: float) -> None:
        if any(dim <= 0 for dim in dimensions):
            raise ValueError('Invalid dimension')

    def get_volume(self) -> float:
        return self.width / 100 * self.height / 100 * self.length / 100
