"""Test pour la console."""

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.auth import AuthManager
from src.core.places import PlaceManager, Place
from src.core.algorithm import GeoPoint
from src.data.storage import JsonStorage


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.auth = AuthManager(JsonStorage("test_users.json"))
    
    def tearDown(self):
        if os.path.exists("test_users.json"):
            os.remove("test_users.json")
    
    def test_register_and_login(self):
        """Register et login."""
        self.auth.register("alice", "pass123")
        user = self.auth.login("alice", "pass123")
        self.assertEqual(user.username, "alice")
        self.assertIsNotNone(self.auth.get_current_user())


class TestPlace(unittest.TestCase):
    def setUp(self):
        self.pm = PlaceManager(JsonStorage("test_places.json"), "alice")
    
    def tearDown(self):
        if os.path.exists("test_places.json"):
            os.remove("test_places.json")
    
    def test_add_remove_place(self):
        """Ajouter et supprimer une place."""
        place = Place("Paris", GeoPoint(48.8566, 2.3522), "alice")
        places = self.pm._load_owner_places()
        places.append(place.to_dict())
        self.pm._save_owner_places(places)
        
        self.assertEqual(len(self.pm.list_places()), 1)
        self.pm.remove_place("Paris")
        self.assertEqual(len(self.pm.list_places()), 0)


if __name__ == "__main__":
    unittest.main()

