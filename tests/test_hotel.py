"""
test_hotel.py — Unit tests for hotel.py (Hotel)

Run with: python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.hotel import Hotel
from src.core.places import Place
from src.core.algorithm import GeoPoint

class TestHotel(unittest.TestCase):

    def setUp(self):
        """Create reusable test data."""
        self.place_paris = Place(name="Paris", point=GeoPoint(lat=48.8566, lon=2.3522), owner="user1")
        self.hotel = Hotel(place=self.place_paris)

    def test_hotel_creation(self):
        """Hotel must store place and distance limit correctly."""
        self.assertEqual(self.hotel.place.name, "Paris")
        self.assertEqual(self.hotel.place.point.lat, 48.8566)
        self.assertEqual(self.hotel.place.point.lon, 2.3522)
        self.assertEqual(self.hotel.nearby_distance_limit, 60.0)

    def test_hotel_custom_distance_limit(self):
        """Hotel must accept custom distance limit."""
        place_lyon = Place(name="Lyon", point=GeoPoint(lat=45.7640, lon=4.8357), owner="user1")
        hotel = Hotel(place=place_lyon, distance_limit=30.0)
        self.assertEqual(hotel.nearby_distance_limit, 30.0)

    def test_set_nearby_cities(self):
        """set_nearby_cities must find cities within distance limit."""
        places = [
            Place(name="Paris", point=GeoPoint(lat=48.8566, lon=2.3522), owner="user1"),
            Place(name="Versailles", point=GeoPoint(lat=48.8049, lon=2.1204), owner="user1"),
            Place(name="Fontainebleau", point=GeoPoint(lat=48.4047, lon=2.6993), owner="user1"),
            Place(name="Lyon", point=GeoPoint(lat=45.7640, lon=4.8357), owner="user1"),
        ]

        nearby = self.hotel.set_nearby_cities(places)

        nearby_names = [p.name for p in nearby]
        self.assertIn("Versailles", nearby_names)
        self.assertIn("Fontainebleau", nearby_names)
        self.assertNotIn("Lyon", nearby_names)
        self.assertNotIn("Paris", nearby_names)

    def test_get_nearby_cities(self):
        """get_nearby_cities must return previously set nearby cities."""
        places = [
            Place(name="Paris", point=GeoPoint(lat=48.8566, lon=2.3522), owner="user1"),
            Place(name="Versailles", point=GeoPoint(lat=48.8049, lon=2.1204), owner="user1"),
        ]

        self.hotel.set_nearby_cities(places)
        nearby = self.hotel.get_nearby_cities()

        self.assertEqual(len(nearby), 1)
        self.assertEqual(nearby[0].name, "Versailles")

    def test_get_nearby_cities_info(self):
        """get_nearby_cities_info must return formatted list sorted by distance."""
        places = [
            Place(name="Paris", point=GeoPoint(lat=48.8566, lon=2.3522), owner="user1"),
            Place(name="Versailles", point=GeoPoint(lat=48.8049, lon=2.1204), owner="user1"),
            Place(name="Fontainebleau", point=GeoPoint(lat=48.4047, lon=2.6993), owner="user1"),
        ]

        self.hotel.set_nearby_cities(places)
        info = self.hotel.get_nearby_cities_info()

        self.assertEqual(len(info), 2)
        self.assertIn("name", info[0])
        self.assertIn("distance_km", info[0])
        self.assertIn("lat", info[0])
        self.assertIn("lon", info[0])

        # Check sorted by distance
        for i in range(len(info) - 1):
            self.assertLessEqual(info[i]["distance_km"], info[i + 1]["distance_km"])

    def test_to_dict(self):
        """to_dict must return dict with place and distance_limit."""
        data = self.hotel.to_dict()

        self.assertIn("place", data)
        self.assertIn("distance_limit", data)
        self.assertEqual(data["place"]["name"], "Paris")
        self.assertEqual(data["distance_limit"], 60.0)

    def test_from_dict(self):
        """from_dict must reconstruct Hotel identical to original."""
        data = self.hotel.to_dict()
        hotel2 = Hotel.from_dict(data)

        self.assertEqual(hotel2.place.name, self.hotel.place.name)
        self.assertEqual(hotel2.place.owner, self.hotel.place.owner)
        self.assertEqual(hotel2.place.point.lat, self.hotel.place.point.lat)
        self.assertEqual(hotel2.place.point.lon, self.hotel.place.point.lon)
        self.assertEqual(hotel2.nearby_distance_limit, self.hotel.nearby_distance_limit)

    def test_repr(self):
        """repr must contain hotel place name and nearby city count."""
        repr_str = repr(self.hotel)

        self.assertIn("Paris", repr_str)
        self.assertIn("Hotel", repr_str)


if __name__ == "__main__":
    unittest.main()
