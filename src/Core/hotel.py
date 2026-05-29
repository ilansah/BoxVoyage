from core.places import Place
from core.algorithm import GeoPoint, DistanceCalculator


class Hotel:
    """
    Represents a hotel in a city with a list of nearby cities within 60km radius.
    
    This allows users to stay in one hotel and make day trips to nearby cities
    instead of changing hotels frequently.
    
    Attributes:
        place (Place): The place representing the hotel location (contains name and coordinates).
        nearby_distance_limit (float): Maximum distance in km to consider a city nearby (default: 60km).
    """
    
    NEARBY_DISTANCE_LIMIT = 60.0  # km
    
    def __init__(self, place: Place, distance_limit: float = NEARBY_DISTANCE_LIMIT):
        """
        Initialize a Hotel.
        
        Args:
            place (Place): The place object representing the hotel location.
            distance_limit (float): Maximum distance in km to consider a city nearby (default: 60km).
        """
        self.place = place
        self.nearby_distance_limit = distance_limit
        self._nearby_cities = []
    
    def set_nearby_cities(self, all_places: list[Place]) -> list[Place]:
        """
        Calculate and set the list of nearby cities within the distance limit.
        
        Args:
            all_places (list[Place]): List of all available places/cities for the user.
        
        Returns:
            list[Place]: List of cities within the distance limit (excluding the hotel location itself).
        """
        nearby = []
        
        for place in all_places:
            # Skip the hotel location itself
            if place.name.lower() == self.place.name.lower():
                continue
            
            # Calculate distance between hotel and the place
            distance = DistanceCalculator.distance(self.place.point, place.point)
            
            # Add to nearby list if within the limit
            if distance <= self.nearby_distance_limit:
                nearby.append(place)
        
        self._nearby_cities = nearby
        return nearby
    
    def get_nearby_cities(self) -> list[Place]:
        """
        Get the list of nearby cities that have been calculated.
        
        Returns:
            list[Place]: List of cities within the distance limit from the hotel.
        """
        return self._nearby_cities
    
    def get_nearby_cities_info(self) -> list[dict]:
        """
        Get formatted information about nearby cities with distances.
        
        Returns:
            list[dict]: List of dictionaries containing city name and distance in km.
        """
        info = []
        for place in self._nearby_cities:
            distance = DistanceCalculator.distance(self.place.point, place.point)
            info.append({
                "name": place.name,
                "distance_km": distance,
                "lat": place.point.lat,
                "lon": place.point.lon
            })
        
        # Sort by distance
        n = len(info)
        for i in range(n):
            for j in range(0, n - i - 1):
                if info[j]["distance_km"] > info[j + 1]["distance_km"]:
                    # Swap
                    temp = info[j]
                    info[j] = info[j + 1]
                    info[j + 1] = temp
        
        return info
    
    def to_dict(self) -> dict:
        """Serializes the Hotel to a JSON-compatible dictionary."""
        return {
            "place": self.place.to_dict(),
            "distance_limit": self.nearby_distance_limit
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Hotel":
        """Deserializes a Hotel from a dictionary (loaded from JSON)."""
        place = Place.from_dict(data["place"])
        distance_limit = data.get("distance_limit", cls.NEARBY_DISTANCE_LIMIT)
        return cls(place=place, distance_limit=distance_limit)
    
    def __repr__(self) -> str:
        return f"Hotel(place={self.place.name!r}, nearby_cities={len(self._nearby_cities)})"

