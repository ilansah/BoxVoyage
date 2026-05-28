"""
tours.py — Tour management.

Handles:
- Tour: data object representing a named trip belonging to a user
- TourManager: CRUD operations on a user's tour list
"""

import uuid

from core.places import Place


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
        self.id = uuid.uuid4().hex[:8]
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
