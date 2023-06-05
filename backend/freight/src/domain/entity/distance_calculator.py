# Domain Service

import math

from freight.src.domain.entity.coordinates import Coordinates


class DistanceCalculator:
    @classmethod
    def calculate(cls, origin: Coordinates, destination: Coordinates) -> float:
        if origin.latitude == destination.latitude and origin.longitude == destination.longitude:
            return 0

        cosine_angle = cls.calculate_cosine_angle(origin, destination)
        central_angle = cls.calculate_central_angle(cosine_angle)
        return cls.calculate_distance_in_kilometers(central_angle)

    @staticmethod
    def calculate_cosine_angle(origin: Coordinates, destination: Coordinates) -> float:
        latitude_origin = math.radians(origin.latitude)
        latitude_destination = math.radians(destination.latitude)
        longitude_diff = math.radians(origin.longitude - destination.longitude)
        cosine_angle = math.sin(latitude_origin) * math.sin(latitude_destination) + math.cos(
            latitude_origin
        ) * math.cos(latitude_destination) * math.cos(longitude_diff)
        return min(cosine_angle, 1)

    @staticmethod
    def calculate_central_angle(cosine_angle: float) -> float:
        return math.acos(cosine_angle)

    @staticmethod
    def calculate_distance_in_kilometers(central_angle: float) -> float:
        central_angle_degrees = math.degrees(central_angle)
        distance_in_miles = central_angle_degrees * 60 * 1.1515
        return distance_in_miles * 1.609344
