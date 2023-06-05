import unittest

from freight.src.domain.entity.coordinates import Coordinates
from freight.src.domain.entity.distance_calculator import DistanceCalculator


class TestDistanceCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.origin = Coordinates(-27.5945, -48.5477)
        self.destination = Coordinates(-22.9129, -43.2003)

    def test_distance_calculation(self) -> None:
        distance = DistanceCalculator.calculate(self.origin, self.destination)
        self.assertEqual(distance, 748.2217780081631)


if __name__ == '__main__':
    unittest.main()
