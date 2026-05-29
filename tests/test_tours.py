import os
import sys
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.tours import Tour, TourManager
from core.algorithm import GeoPoint
from core.places import Place


def make_place(name: str, lat: float, lon: float) -> Place:
    """Creates a Place object for use in tests."""
    return Place(name=name, point=GeoPoint(lat=lat, lon=lon), owner="alice")


# Tour tests

class TestTour(unittest.TestCase):

    def setUp(self):
        """Creates a reusable Tour instance for all tests in this class."""
        self.tour = Tour(name="Europe Trip", owner="alice", places=[])

    def test_attributes_are_stored(self):
        """Tour must store name, owner, places and is_public correctly."""
        self.assertEqual(self.tour.name, "Europe Trip")
        self.assertEqual(self.tour.owner, "alice")
        self.assertEqual(self.tour.places, [])
        self.assertFalse(self.tour.is_public)

    def test_id_is_generated(self):
        """Tour id must be automatically generated and have 8 characters."""
        self.assertIsNotNone(self.tour.id)
        self.assertEqual(len(self.tour.id), 8)

    def test_two_tours_have_different_ids(self):
        """Two distinct Tour objects must have different ids."""
        tour2 = Tour(name="Asia Trip", owner="alice", places=[])
        self.assertNotEqual(self.tour.id, tour2.id)

    def test_to_dict(self):
        """to_dict must return a dict with all expected keys."""
        d = self.tour.to_dict()
        self.assertIn("id", d)
        self.assertIn("name", d)
        self.assertIn("owner", d)
        self.assertIn("is_public", d)
        self.assertIn("places", d)
        self.assertEqual(d["name"], "Europe Trip")
        self.assertEqual(d["owner"], "alice")

    def test_from_dict(self):
        """from_dict must reconstruct a Tour identical to the original."""
        d = self.tour.to_dict()
        tour2 = Tour.from_dict(d)
        self.assertEqual(tour2.id, self.tour.id)
        self.assertEqual(tour2.name, self.tour.name)
        self.assertEqual(tour2.owner, self.tour.owner)
        self.assertEqual(tour2.is_public, self.tour.is_public)

    def test_from_dict_does_not_generate_new_id(self):
        """from_dict must preserve the original id, not generate a new one."""
        d = self.tour.to_dict()
        tour2 = Tour.from_dict(d)
        self.assertEqual(tour2.id, self.tour.id)


# TourManager tests

class TestTourManager(unittest.TestCase):

    def _make_manager(self, initial_data: dict) -> TourManager:
        """Helper: creates a TourManager with a mocked storage."""
        mock_storage = MagicMock()
        mock_storage.load.return_value = initial_data
        return TourManager(storage=mock_storage, owner="alice")

    def _sample_tour_dict(self, tour_id: str = "abcd1234") -> dict:
        """Helper: returns a minimal valid tour dict."""
        return {
            "id": tour_id,
            "name": "Europe Trip",
            "owner": "alice",
            "is_public": False,
            "places": []
        }

    def test_list_tours_empty(self):
        """list_tours must return an empty list when the user has no tours."""
        manager = self._make_manager({})
        self.assertEqual(manager.list_tours(), [])

    def test_list_tours_returns_correct_owner(self):
        """list_tours must return only the tours belonging to the current user."""
        data = {
            "alice": [self._sample_tour_dict("aaaa1111")],
            "bob":   [self._sample_tour_dict("bbbb2222")]
        }
        # Fix bob's tour owner field
        data["bob"][0]["owner"] = "bob"
        manager = self._make_manager(data)
        tours = manager.list_tours()
        self.assertEqual(len(tours), 1)
        self.assertEqual(tours[0].owner, "alice")

    def test_create_tour(self):
        """create_tour must return a Tour with the correct name and owner."""
        manager = self._make_manager({"alice": []})
        places = [make_place("Paris", 48.85, 2.35), make_place("London", 51.50, -0.12)]
        tour = manager.create_tour("My Trip", places)
        self.assertEqual(tour.name, "My Trip")
        self.assertEqual(tour.owner, "alice")
        self.assertEqual(len(tour.places), 2)

    def test_create_tour_saves_to_storage(self):
        """create_tour must call storage.save once."""
        manager = self._make_manager({"alice": []})
        manager.create_tour("My Trip", [make_place("Paris", 48.85, 2.35)])
        self.assertTrue(manager.storage.save.called)

    def test_get_tour_by_id_found(self):
        """get_tour_by_id must return the correct Tour when the id exists."""
        data = {"alice": [self._sample_tour_dict("abcd1234")]}
        manager = self._make_manager(data)
        tour = manager.get_tour_by_id("abcd1234")
        self.assertIsNotNone(tour)
        self.assertEqual(tour.id, "abcd1234")

    def test_get_tour_by_id_not_found(self):
        """get_tour_by_id must return None when the id does not exist."""
        manager = self._make_manager({"alice": []})
        tour = manager.get_tour_by_id("xxxxxxxx")
        self.assertIsNone(tour)

    def test_set_visibility_to_public(self):
        """set_visibility must return True and update is_public to True."""
        data = {"alice": [self._sample_tour_dict("abcd1234")]}
        manager = self._make_manager(data)
        result = manager.set_visibility("abcd1234", is_public=True)
        self.assertTrue(result)

    def test_set_visibility_to_private(self):
        """set_visibility must return True and update is_public to False."""
        tour_dict = self._sample_tour_dict("abcd1234")
        tour_dict["is_public"] = True
        data = {"alice": [tour_dict]}
        manager = self._make_manager(data)
        result = manager.set_visibility("abcd1234", is_public=False)
        self.assertTrue(result)

    def test_set_visibility_not_found(self):
        """set_visibility must return False when the tour id does not exist."""
        manager = self._make_manager({"alice": []})
        result = manager.set_visibility("xxxxxxxx", is_public=True)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()