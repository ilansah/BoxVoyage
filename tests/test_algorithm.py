import math
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.algorithm import GeoPoint, DistanceCalculator, TourOptimiszer


class TestGeoPoint(unittest.TestCase):
    """Tests for the GeoPoint class."""

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

    def test_repr(self):
        """Test string representation of GeoPoint."""
        point = GeoPoint(lat=35.682, lon=139.762)
        self.assertEqual(repr(point), "GeoPoint(lat=35.682, lon=139.762)")


class TestDistanceCalculator(unittest.TestCase):
    """Tests for the DistanceCalculator class."""

    def test_same_point_distance_is_zero(self):
        """Distance between identical points must be zero."""
        point = GeoPoint(lat=48.8566, lon=2.3522)
        distance = DistanceCalculator.distance(point, point)
        self.assertAlmostEqual(distance, 0.0, places=3)

    def test_paris_london_distance(self):
        """Test distance between Paris and London (approximately 343.9 km)."""
        paris = GeoPoint(lat=48.8566, lon=2.3522)
        london = GeoPoint(lat=51.5074, lon=-0.1278)
        distance = DistanceCalculator.distance(paris, london)
        # Expected distance is approximately 343.94 km
        self.assertAlmostEqual(distance, 343.94, delta=1.0)

    def test_equator_distance(self):
        """Test distance along the equator."""
        point1 = GeoPoint(lat=0.0, lon=0.0)
        point2 = GeoPoint(lat=0.0, lon=1.0)
        distance = DistanceCalculator.distance(point1, point2)
        # Approximately 111.32 km per degree at equator
        self.assertAlmostEqual(distance, 111.32, delta=1.0)

    def test_north_pole_distance(self):
        """Test distance to north pole."""
        point = GeoPoint(lat=0.0, lon=0.0)
        north_pole = GeoPoint(lat=90.0, lon=0.0)
        distance = DistanceCalculator.distance(point, north_pole)
        # Distance from equator to north pole is quarter of Earth's circumference
        expected = (2 * math.pi * 6378.197) / 4
        self.assertAlmostEqual(distance, expected, delta=1.0)

    def test_distance_symmetry(self):
        """Distance from A to B must equal distance from B to A."""
        tokyo = GeoPoint(lat=35.682, lon=139.762)
        sydney = GeoPoint(lat=-33.8688, lon=151.2093)
        dist1 = DistanceCalculator.distance(tokyo, sydney)
        dist2 = DistanceCalculator.distance(sydney, tokyo)
        self.assertAlmostEqual(dist1, dist2, places=5)

    def test_earth_radius_constant(self):
        """Test that Earth radius constant is correct."""
        self.assertEqual(DistanceCalculator.EARTH_RADIUS, 6378.197)

    def test_antipodal_points(self):
        """Test distance between antipodal points (opposite sides of Earth)."""
        north = GeoPoint(lat=0.0, lon=0.0)
        south = GeoPoint(lat=0.0, lon=180.0)
        distance = DistanceCalculator.distance(north, south)
        # Distance should be half of Earth's circumference
        expected = math.pi * 6378.197
        self.assertAlmostEqual(distance, expected, delta=1.0)

    def test_total_tour(self):
        tokyo = GeoPoint(lat=35.682, lon=139.762)
        sydney = GeoPoint(lat=-33.8688, lon=151.2093)
        south = GeoPoint(lat=0.0, lon=180.0)
        list = []
        list.append(tokyo)
        list.append(sydney)
        list.append(south)
        tour = TourOptimiszer.calculate_tour_distance(list)
        self.assertAlmostEqual(tour, 18407.597305933155)


if __name__ == "__main__":
    unittest.main()