import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.places import Place, GeocodingService, PlaceManager
from core.algorithm import GeoPoint
from data.storage import JsonStorage


class TestPlace(unittest.TestCase):
    """Tests for the Place class."""

    def test_place_creation(self):
        """Test creating a Place with GeoPoint."""
        point = GeoPoint(lat=48.8566, lon=2.3522)
        place = Place(name="Eiffel Tower", point=point, owner="alice")
        self.assertEqual(place.name, "Eiffel Tower")
        self.assertEqual(place.point.lat, 48.8566)
        self.assertEqual(place.point.lon, 2.3522)
        self.assertEqual(place.owner, "alice")

    def test_place_to_dict(self):
        """Test serialization of Place to dictionary."""
        point = GeoPoint(lat=48.8566, lon=2.3522)
        place = Place(name="Eiffel Tower", point=point, owner="alice")
        place_dict = place.to_dict()
        self.assertEqual(place_dict["name"], "Eiffel Tower")
        self.assertEqual(place_dict["lat"], 48.8566)
        self.assertEqual(place_dict["lon"], 2.3522)
        self.assertEqual(place_dict["owner"], "alice")

    def test_place_from_dict(self):
        """Test deserialization of Place from dictionary."""
        place_dict = {
            "name": "Eiffel Tower",
            "lat": 48.8566,
            "lon": 2.3522,
            "owner": "alice"
        }
        place = Place.from_dict(place_dict)
        self.assertEqual(place.name, "Eiffel Tower")
        self.assertEqual(place.point.lat, 48.8566)
        self.assertEqual(place.point.lon, 2.3522)
        self.assertEqual(place.owner, "alice")

    def test_place_repr(self):
        """Test string representation of Place."""
        point = GeoPoint(lat=48.8566, lon=2.3522)
        place = Place(name="Eiffel Tower", point=point, owner="alice")
        repr_str = repr(place)
        self.assertIn("Eiffel Tower", repr_str)
        self.assertIn("48.8566", repr_str)
        self.assertIn("2.3522", repr_str)


class TestGeocodingService(unittest.TestCase):
    """Tests for the GeocodingService class using real Nominatim API."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = GeocodingService()

    def test_get_coordinates_paris(self):
        """Test getting coordinates for Paris using real Nominatim API."""
        result = self.service.get_coordinates("Paris, France")
        self.assertIsNotNone(result)
        # Paris should be around these coordinates
        self.assertAlmostEqual(result.lat, 48.8566, delta=0.1)
        self.assertAlmostEqual(result.lon, 2.3522, delta=0.1)

    def test_get_coordinates_london(self):
        """Test getting coordinates for London using real Nominatim API."""
        result = self.service.get_coordinates("London, UK")
        self.assertIsNotNone(result)
        # London should be around these coordinates
        self.assertAlmostEqual(result.lat, 51.5074, delta=0.1)
        self.assertAlmostEqual(result.lon, -0.1278, delta=0.1)

    def test_get_coordinates_new_york(self):
        """Test getting coordinates for New York using real Nominatim API."""
        result = self.service.get_coordinates("New York, USA")
        self.assertIsNotNone(result)
        # New York should be around these coordinates
        self.assertAlmostEqual(result.lat, 40.7128, delta=0.1)
        self.assertAlmostEqual(result.lon, -74.0060, delta=0.1)

    def test_get_coordinates_tokyo(self):
        """Test getting coordinates for Tokyo using real Nominatim API."""
        result = self.service.get_coordinates("Tokyo, Japan")
        self.assertIsNotNone(result)
        # Tokyo should be around these coordinates
        self.assertAlmostEqual(result.lat, 35.682, delta=0.1)
        self.assertAlmostEqual(result.lon, 139.762, delta=0.1)

    def test_get_coordinates_sydney(self):
        """Test getting coordinates for Sydney using real Nominatim API."""
        result = self.service.get_coordinates("Sydney, Australia")
        self.assertIsNotNone(result)
        # Sydney should be around these coordinates
        self.assertAlmostEqual(result.lat, -33.8688, delta=0.1)
        self.assertAlmostEqual(result.lon, 151.2093, delta=0.1)

    def test_get_coordinates_berlin(self):
        """Test getting coordinates for Berlin using real Nominatim API."""
        result = self.service.get_coordinates("Berlin, Germany")
        self.assertIsNotNone(result)
        # Berlin should be around these coordinates
        self.assertAlmostEqual(result.lat, 52.52, delta=0.1)
        self.assertAlmostEqual(result.lon, 13.405, delta=0.1)

    def test_get_coordinates_returns_geopoint(self):
        """Test that get_coordinates returns a GeoPoint object with valid properties."""
        result = self.service.get_coordinates("Rome, Italy")
        self.assertIsNotNone(result)
        # Verify that GeoPoint properties work correctly
        self.assertTrue(hasattr(result, 'lat'))
        self.assertTrue(hasattr(result, 'lon'))
        self.assertTrue(hasattr(result, 'lat_rad'))
        self.assertTrue(hasattr(result, 'lon_rad'))
        self.assertIsNotNone(result.lat_rad)
        self.assertIsNotNone(result.lon_rad)

    def test_get_coordinates_invalid_address(self):
        """Test getting coordinates for an invalid address."""
        result = self.service.get_coordinates("InvalidPlaceName123456789XYZ")
        # Invalid address should return None
        self.assertIsNone(result)


class TestPlaceIntegration(unittest.TestCase):
    """Integration tests for Place-related functionality."""

    def test_geocoding_to_place_workflow(self):
        """Test workflow of geocoding an address and creating a Place."""
        service = GeocodingService()
        coords = service.get_coordinates("Paris, France")
        
        self.assertIsNotNone(coords)
        
        # Create a Place from the geocoded coordinates
        place = Place(name="My Paris Visit", point=coords, owner="alice")
        
        self.assertEqual(place.name, "My Paris Visit")
        self.assertAlmostEqual(place.point.lat, 48.8566, delta=0.1)
        self.assertAlmostEqual(place.point.lon, 2.3522, delta=0.1)

    def test_place_serialization_roundtrip(self):
        """Test that Place can be serialized and deserialized without loss."""
        point = GeoPoint(lat=48.8566, lon=2.3522)
        original_place = Place(name="Eiffel Tower", point=point, owner="alice")
        
        # Serialize
        place_dict = original_place.to_dict()
        
        # Deserialize
        restored_place = Place.from_dict(place_dict)
        
        # Verify
        self.assertEqual(original_place.name, restored_place.name)
        self.assertEqual(original_place.point.lat, restored_place.point.lat)
        self.assertEqual(original_place.point.lon, restored_place.point.lon)
        self.assertEqual(original_place.owner, restored_place.owner)

    def test_geocoding_multiple_locations(self):
        """Test geocoding multiple locations."""
        service = GeocodingService()
        locations = ["Paris, France", "London, UK", "New York, USA"]
        
        places = []
        for location in locations:
            coords = service.get_coordinates(location)
            self.assertIsNotNone(coords, f"Failed to geocode {location}")
            place = Place(name=location, point=coords, owner="alice")
            places.append(place)
        
        self.assertEqual(len(places), 3)
        
        # Verify all places were created correctly
        for place in places:
            self.assertIsNotNone(place.point)
            self.assertIsNotNone(place.point.lat)
            self.assertIsNotNone(place.point.lon)


if __name__ == "__main__":
    unittest.main()
