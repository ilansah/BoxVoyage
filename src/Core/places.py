"""
places.py — Place management and geographic geocoding.

Handles:
- GeoPoint: geographic coordinate representation (placeholder, will be replaced
  by the import from algorithm.py once P2 delivers their part)
- GeocodingService: converts a place name to coordinates via Nominatim API
- Place: data object representing a user's place of interest
- PlaceManager: CRUD operations on a user's place list
"""

import json
import math
import os
import requests
from src.core.algorithm import GeoPoint
from geopy.geocoders import Nominatim
from src.data.storage import JsonStorage


class Place:
    """
    Represents a place of interest belonging to a user.

    Attributes:
        name (str): Display name of the place (as entered by the user).
        point (GeoPoint): Geographic coordinates of the place.
        owner (str): Username of the user who added this place.
    """

    def __init__(self, name: str, point: GeoPoint, owner: str):
        self.name = name
        self.point = point
        self.owner = owner

    def to_dict(self) -> dict:
        """Serializes the Place to a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "lat": self.point.lat,
            "lon": self.point.lon,
            "owner": self.owner,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Place":
        """Deserializes a Place from a dictionary (loaded from JSON)."""
        point = GeoPoint(lat=data["lat"], lon=data["lon"])
        return cls(name=data["name"], point=point, owner=data["owner"])

    def __repr__(self) -> str:
        return f"Place(name={self.name!r}, lat={self.point.lat}, lon={self.point.lon})"




from src.core.algorithm import GeoPoint

class GeocodingService:
    """
    Service for geocoding addresses to geographic coordinates.
    Uses Nominatim (OpenStreetMap) as the geocoding provider.
    """

    def __init__(self):
        self.geocoder = Nominatim(user_agent="boxvoyage")

    def get_coordinates(self, address: str) -> GeoPoint | None:
        """
        Get latitude and longitude for a given address.

        Args:
            address (str): The address to geocode.

        Returns:
            GeoPoint if found, None otherwise.
        """
        location = self.geocoder.geocode(address)
        if location is None:
            return None
        return GeoPoint(lat=location.latitude, lon=location.longitude)

  
class PlaceManager:
    """
    Manages CRUD operations on a user's list of places.

    Places are stored in JSON file

    Args:
        storage (JsonStorage): Storage instance pointing to places.json.
        owner (str): Username of the currently logged-in user.
    """

    def __init__(self, storage, owner: str):
        self.storage = storage
        self.owner = owner

    def _load_owner_places(self) -> list[dict]:
        """Returns the raw place dicts for the current user."""
        data = self.storage.load()
        return data.get(self.owner, [])

    def _save_owner_places(self, places: list[dict]) -> None:
        """Overwrites the current user's place list in storage."""
        data = self.storage.load()
        data[self.owner] = places
        self.storage.save(data)

    def search_and_add(self, name: str) -> "Place | None":
        """
        Geocodes the given name and adds it to the user's place list.
        Returns the Place if successful, None if not found or duplicate.
        """
        existing = self._load_owner_places()

        # Prevent duplicates (case-insensitive)
        if any(p["name"].lower() == name.lower() for p in existing):
            print(f"[INFO] '{name}' is already in your list.")
            return None

        service = GeocodingService()
        point = service.get_coordinates(name)

        if point is None:
            print(f"[ERROR] Could not find coordinates for '{name}'.")
            return None

        place = Place(name=name, point=point, owner=self.owner)
        existing.append(place.to_dict())
        self._save_owner_places(existing)
        return place