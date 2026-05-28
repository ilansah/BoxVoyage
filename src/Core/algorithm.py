import math

class GeoPoint:
    """
    Represents a geographic point using decimal degree coordinates (DD format).

    Attributes:
        lat (float): Latitude in decimal degrees (e.g. 35.682 for Tokyo)
        lon (float): Longitude in decimal degrees (e.g. 139.762 for Tokyo)

    Properties:
        lat_rad (float): Latitude converted to radians (required by the distance formula)
        lon_rad (float): Longitude converted to radians
    """

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    @property
    def lat_rad(self) -> float:
        return self.lat * math.pi / 180

    @property
    def lon_rad(self) -> float:
        return self.lon * math.pi / 180

    def __repr__(self) -> str:
        return f"GeoPoint(lat={self.lat}, lon={self.lon})"


class DistanceCalculator:
    """
    Calculates distances between geographic points using the great-circle distance formula.
    
    Constants:
        EARTH_RADIUS (float): Radius of Earth in kilometers = 6378.197 km
        PI (float): Mathematical constant π = 3.141592
    """
    
    EARTH_RADIUS = 6378.197  # km
    PI = 3.141592
    
    @staticmethod
    def distance(point1: GeoPoint, point2: GeoPoint) -> float:
        """
        Calculate the great-circle distance between two geographic points.
        
        Formula:
            D(lat₁, lon₁) = R_terre × arccos(sin(lat₁) × sin(lat₂) + cos(lat₁) × cos(lat₂) × cos(lon₂ - lon₁))
        
        Args:
            point1 (GeoPoint): First geographic point
            point2 (GeoPoint): Second geographic point
        
        Returns:
            float: Distance in kilometers
        """
        lat1_rad = point1.lat_rad
        lon1_rad = point1.lon_rad
        lat2_rad = point2.lat_rad
        lon2_rad = point2.lon_rad
        
        # Apply the great-circle distance formula
        cos_angle = (
            math.sin(lat1_rad) * math.sin(lat2_rad) +
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad)
        )
        
        # Clamp to [-1, 1] to avoid numerical errors with arccos
        cos_angle = max(-1, min(1, cos_angle))
        
        distance = DistanceCalculator.EARTH_RADIUS * math.acos(cos_angle)
        return distance

# Test the distance calculator
point1 = GeoPoint(48.8566, 2.3522)  # Paris
point2 = GeoPoint(51.5074, -0.1278)  # London
result = DistanceCalculator.distance(point1, point2)
print(f"Distance between Paris and London: {result:.2f} km")