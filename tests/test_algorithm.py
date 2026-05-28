import math
import unittest
from src.Core.algorithm import GeoPoint

class TestGeoPoint(unittest.TestCase):

    def test_attributes_are_stored(self):
        """lat and lon passed to the constructor"""
        point = GeoPoint(lat=35.682, lon=139.762)
        self.assertEqual(point.lat, 35.682)
        self.assertEqual(point.lon, 139.762)

    def test_lat_rad_conversion(self):
        """lat_rad must equal lat * pi / 180."""
        point = GeoPoint(lat=90.0, lon=0.0)
        self.assertAlmostEqual(point.lat_rad, math.pi / 2, places=9)

    def test_lon_rad_conversion(self):
        """lon_rad must equal lon * pi / 180."""
        point = GeoPoint(lat=0.0, lon=180.0)
        self.assertAlmostEqual(point.lon_rad, math.pi, places=9)

    def test_zero_coordinates(self):
        """GeoPoint(0, 0) must give lat_rad = 0.0 and lon_rad = 0.0."""
        point = GeoPoint(lat=0.0, lon=0.0)
        self.assertEqual(point.lat_rad, 0.0)
        self.assertEqual(point.lon_rad, 0.0)

    def test_negative_coordinates(self):
        """Negative coordinates (southern/western hemisphere) must convert correctly."""
        point = GeoPoint(lat=-45.0, lon=-90.0)
        self.assertAlmostEqual(point.lat_rad, -math.pi / 4, places=9)
        self.assertAlmostEqual(point.lon_rad, -math.pi / 2, places=9)


if __name__ == "__main__":
    unittest.main()