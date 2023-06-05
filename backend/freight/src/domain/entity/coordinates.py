# Value Object


class Coordinates:
    def __init__(self, latitude: float, longitude: float) -> None:
        if not self._are_valid_coordinates(latitude, longitude):
            raise ValueError('Invalid coordinates provided.')
        self.latitude = latitude
        self.longitude = longitude

    def _are_valid_coordinates(self, latitude: float, longitude: float) -> bool:
        return -90 <= latitude <= 90 and -180 <= longitude <= 180  # noqa: PLR2004
