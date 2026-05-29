"""
test_places.py — Unit tests for places.py (Place, GeocodingService, PlaceManager)

Run with: python -m unittest discover -s tests -v
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.places import Place, PlaceManager, GeocodingService
from src.core.algorithm import GeoPoint


# Place tests

class TestPlace(unittest.TestCase):

    def setUp(self):
        """Creates a reusable Place instance for all tests in this class."""
        self.point = GeoPoint(lat=48.8566, lon=2.3522)
        self.place = Place(name="Eiffel Tower", point=self.point, owner="alice")

    def test_attributes_are_stored(self):
        """Place must store name, point and owner correctly."""
        self.assertEqual(self.place.name, "Eiffel Tower")
        self.assertEqual(self.place.owner, "alice")
        self.assertEqual(self.place.point.lat, 48.8566)
        self.assertEqual(self.place.point.lon, 2.3522)

    def test_to_dict(self):
        """to_dict must return a dict with name, lat, lon, owner."""
        d = self.place.to_dict()
        self.assertEqual(d["name"], "Eiffel Tower")
        self.assertEqual(d["lat"], 48.8566)
        self.assertEqual(d["lon"], 2.3522)
        self.assertEqual(d["owner"], "alice")

    def test_from_dict(self):
        """from_dict must reconstruct a Place identical to the original."""
        d = self.place.to_dict()
        place2 = Place.from_dict(d)
        self.assertEqual(place2.name, self.place.name)
        self.assertEqual(place2.owner, self.place.owner)
        self.assertEqual(place2.point.lat, self.place.point.lat)
        self.assertEqual(place2.point.lon, self.place.point.lon)

    def test_roundtrip_to_dict_from_dict(self):
        """A Place converted to dict and back must be identical."""
        place2 = Place.from_dict(self.place.to_dict())
        self.assertEqual(place2.name, self.place.name)
        self.assertEqual(place2.point.lat, self.place.point.lat)

    def test_repr(self):
        """repr must contain the name and coordinates."""
        r = repr(self.place)
        self.assertIn("Eiffel Tower", r)
        self.assertIn("48.8566", r)
        self.assertIn("2.3522", r)


# PlaceManager tests (with mocked storage — no file system required)

class TestPlaceManager(unittest.TestCase):

    def _make_manager(self, initial_data: dict) -> PlaceManager:
        """Helper: creates a PlaceManager with a mocked storage."""
        mock_storage = MagicMock()
        mock_storage.load.return_value = initial_data
        return PlaceManager(storage=mock_storage, owner="alice")

    def test_list_places_empty(self):
        """list_places must return an empty list when the user has no places."""
        manager = self._make_manager({})
        self.assertEqual(manager.list_places(), [])

    def test_list_places_returns_correct_owner(self):
        """list_places must return only the places belonging to the current user."""
        data = {
            "alice": [{"name": "Paris", "lat": 48.85, "lon": 2.35, "owner": "alice"}],
            "bob":   [{"name": "London", "lat": 51.50, "lon": -0.12, "owner": "bob"}]
        }
        manager = self._make_manager(data)
        places = manager.list_places()
        self.assertEqual(len(places), 1)
        self.assertEqual(places[0].name, "Paris")

    def test_list_places_returns_place_objects(self):
        """list_places must return Place objects, not raw dicts."""
        data = {
            "alice": [{"name": "Paris", "lat": 48.85, "lon": 2.35, "owner": "alice"}]
        }
        manager = self._make_manager(data)
        places = manager.list_places()
        self.assertIsInstance(places[0], Place)

    def test_remove_place_existing(self):
        """remove_place must return True when the place exists."""
        data = {
            "alice": [{"name": "Paris", "lat": 48.85, "lon": 2.35, "owner": "alice"}]
        }
        manager = self._make_manager(data)
        result = manager.remove_place("Paris")
        self.assertTrue(result)

    def test_remove_place_not_found(self):
        """remove_place must return False when the place does not exist."""
        manager = self._make_manager({"alice": []})
        result = manager.remove_place("Paris")
        self.assertFalse(result)

    def test_remove_place_case_insensitive(self):
        """remove_place must work regardless of the case of the name."""
        data = {
            "alice": [{"name": "Paris", "lat": 48.85, "lon": 2.35, "owner": "alice"}]
        }
        manager = self._make_manager(data)
        result = manager.remove_place("paris")
        self.assertTrue(result)

    def test_search_and_add_duplicate(self):
        """search_and_add must return None if the place is already in the list."""
        data = {
            "alice": [{"name": "Paris", "lat": 48.85, "lon": 2.35, "owner": "alice"}]
        }
        manager = self._make_manager(data)
        result = manager.search_and_add("Paris")
        self.assertIsNone(result)

    def test_search_and_add_geocoding_fails(self):
        """search_and_add must return None if GeocodingService returns None."""
        manager = self._make_manager({"alice": []})

        mock_service = MagicMock()
        mock_service.get_coordinates.return_value = None

        with patch("src.core.places.GeocodingService", return_value=mock_service):
            result = manager.search_and_add("UnknownCity")

        self.assertIsNone(result)

    def test_search_and_add_success(self):
        """search_and_add must return a Place when geocoding succeeds."""
        manager = self._make_manager({"alice": []})

        mock_service = MagicMock()
        mock_service.get_coordinates.return_value = GeoPoint(lat=48.85, lon=2.35)

        with patch("src.core.places.GeocodingService", return_value=mock_service):
            result = manager.search_and_add("Paris")

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Paris")
        self.assertEqual(result.owner, "alice")

    def test_search_and_add_saves_to_storage(self):
        """search_and_add must call storage.save when a place is added."""
        manager = self._make_manager({"alice": []})

        mock_service = MagicMock()
        mock_service.get_coordinates.return_value = GeoPoint(lat=48.85, lon=2.35)

        with patch("src.core.places.GeocodingService", return_value=mock_service):
            manager.search_and_add("Paris")

        self.assertTrue(manager.storage.save.called)


if __name__ == "__main__":
    unittest.main()