"""
tours.py — Tour management.

Handles:
- Tour: data object representing a named trip belonging to a user
- TourManager: CRUD operations on a user's tour list
"""

import uuid

from src.core.places import Place


class Tour:
    """
    Represents a named trip belonging to a user.

    Attributes:
        id (str): Unique identifier generated automatically.
        name (str): Name chosen by the user.
        owner (str): Username of the user who created the tour.
        places (list[dict]): Ordered list of places in the tour (stored as dicts).
        is_public (bool): Whether the tour is visible to other users.
    """

    def __init__(self, name: str, owner: str, places: list, is_public: bool = False):
        self.id = uuid.uuid4().hex[:8]  # short unique id, e.g. "a1b2c3d4"
        self.name = name
        self.owner = owner
        self.places = places
        self.is_public = is_public

    def to_dict(self) -> dict:
        """Serializes the Tour to a JSON-compatible dictionary."""
        result = {}
        result["id"] = self.id
        result["name"] = self.name
        result["owner"] = self.owner
        result["is_public"] = self.is_public
        result["places"] = self.places
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "Tour":
        """Deserializes a Tour from a dictionary (loaded from JSON)."""
        # Build the object without calling __init__ to avoid generating a new id
        tour = cls.__new__(cls)
        tour.id = data["id"]
        tour.name = data["name"]
        tour.owner = data["owner"]
        tour.is_public = data["is_public"]
        tour.places = data["places"]
        return tour

    def __repr__(self) -> str:
        return f"Tour(id={self.id!r}, name={self.name!r}, owner={self.owner!r}, places={len(self.places)})"


class TourManager:
    """
    Manages CRUD operations on a user's list of tours.

    Tours are stored in a JSON file structured as:
    { "alice": [ {tour_dict}, ... ], "bob": [ ... ] }

    Args:
        storage: Storage instance pointing to tours.json.
        owner (str): Username of the currently logged-in user.
    """

    def __init__(self, storage, owner: str):
        self.storage = storage
        self.owner = owner

    def _load_owner_tours(self) -> list[dict]:
        """Returns the raw tour dicts for the current user."""
        data = self.storage.load()
        if self.owner not in data:
            return []
        return data[self.owner]

    def _save_owner_tours(self, tours: list[dict]) -> None:
        """Overwrites the current user's tour list in storage."""
        data = self.storage.load()
        data[self.owner] = tours
        self.storage.save(data)

    def create_tour(self, name: str, places: list) -> Tour:
        """
        Creates a new tour with the given name and list of places, then saves it.

        Args:
            name (str): Name chosen by the user for this tour.
            places (list): List of Place objects to include in the tour.

        Returns:
            Tour: The newly created tour.
        """
        # Convert Place objects to dicts for storage
        places_as_dicts = []
        for place in places:
            places_as_dicts.append(place.to_dict())

        tour = Tour(name=name, owner=self.owner, places=places_as_dicts)

        existing = self._load_owner_tours()
        existing.append(tour.to_dict())
        self._save_owner_tours(existing)

        return tour

    def list_tours(self) -> list[Tour]:
        """Returns all tours belonging to the current user."""
        raw_tours = self._load_owner_tours()
        result = []
        for t in raw_tours:
            result.append(Tour.from_dict(t))
        return result

    def get_tour_by_id(self, tour_id: str) -> Tour | None:
        """
        Returns the tour matching the given id, or None if not found.

        Args:
            tour_id (str): The id to look up.
        """
        raw_tours = self._load_owner_tours()
        for t in raw_tours:
            if t["id"] == tour_id:
                return Tour.from_dict(t)
        return None

    def set_visibility(self, tour_id: str, is_public: bool) -> bool:
        """
        Sets the visibility of a tour (public or private).

        Args:
            tour_id (str): The id of the tour to update.
            is_public (bool): True to make it public, False to make it private.

        Returns:
            bool: True if the tour was found and updated, False otherwise.
        """
        raw_tours = self._load_owner_tours()

        for t in raw_tours:
            if t["id"] == tour_id:
                t["is_public"] = is_public
                self._save_owner_tours(raw_tours)
                return True

        return False
    
    def add_place_to_tour(self, tour_id: str, place) -> bool:
        """
        Adds a place to an existing tour.

        Args:
            tour_id (str): The id of the tour to update.
            place: A Place object to add.

        Returns:
            bool: True if the place was added, False if tour not found.
        """
        raw_tours = self._load_owner_tours()

        for t in raw_tours:
            if t["id"] == tour_id:
                t["places"].append(place.to_dict())
                self._save_owner_tours(raw_tours)
                return True

        return False
    
    def update_tour_places(self, tour_id: str, places: list) -> bool:
        """
        Updates the places list of a tour.

        Args:
            tour_id (str): The id of the tour to update.
            places (list): New list of places (as dicts or Place objects).

        Returns:
            bool: True if the tour was found and updated, False otherwise.
        """
        raw_tours = self._load_owner_tours()

        for t in raw_tours:
            if t["id"] == tour_id:
                # Convert Place objects to dicts if needed
                places_as_dicts = []
                for p in places:
                    if isinstance(p, dict):
                        places_as_dicts.append(p)
                    else:
                        places_as_dicts.append(p.to_dict())
                
                t["places"] = places_as_dicts
                self._save_owner_tours(raw_tours)
                return True

        return False