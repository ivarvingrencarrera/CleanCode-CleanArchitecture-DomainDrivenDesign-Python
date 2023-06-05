from freight.src.domain.entity.coordinates import Coordinates


class ZIPCode:
    def __init__(self, code: str, latitude: float, longitude: float) -> None:
        self.code = code
        self.coordinates = Coordinates(latitude, longitude)
