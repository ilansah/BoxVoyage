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


class TourOptimiszer:
    """
    Optimizes tours through multiple geographic points using Nearest Neighbor.
    
    This class works with GeoPoint objects and uses DistanceCalculator to compute distances.
    """

    @staticmethod
    def nearest_neighbor(cities: list[GeoPoint], start_point: GeoPoint = None) -> list[GeoPoint]:
        """
        Finds the optimal tour order using Nearest Neighbor algorithm.
        
        Returns the cities sorted in tour order, starting from start_point and returning to it.
        
        Args:
            cities (list[GeoPoint]): List of all cities to visit
            start_point (GeoPoint): Starting city (default: first city in list)
        
        Returns:
            list[GeoPoint]: Cities in tour order (first city = last city for return trip)
                           Example: [Paris, London, Berlin, Paris]
        """
        if not cities:
            return []
        
        # Use first city as default starting point
        if start_point is None:
            start_point = cities[0]
        
        # Initialize
        unvisited = set(cities)  # Cities not yet visited
        current = start_point    # Current city
        tour = [current]         # Tour path starting with start_point
        unvisited.remove(current)  # Mark as visited
        
        # Build the tour greedily: always go to the nearest unvisited city
        while unvisited:
            # Find nearest unvisited city
            best_city = None
            best_distance = float('inf')
            
            for city in unvisited:
                dist = DistanceCalculator.distance(current, city)
                if dist < best_distance:
                    best_distance = dist
                    best_city = city
            
            # Go to nearest city
            tour.append(best_city)
            unvisited.remove(best_city)
            current = best_city
        
        # Return to starting point
        tour.append(start_point)
        
        return tour

    @staticmethod
    def calculate_tour_distance(tour: list[GeoPoint]) -> float:
        """
        Calculates the total distance of a tour.
        
        Args:
            tour (list[GeoPoint]): Cities in tour order
        
        Returns:
            float: Total distance in kilometers
        """
        total_tour = 0.00
        for i in range(len(tour)-1):
            v1 = tour[i]
            v2 = tour[i+1]
            total_tour += DistanceCalculator.distance(v1,v2)
        total_tour += DistanceCalculator.distance(tour[-1],tour[0])
        return total_tour
    
    @staticmethod
    def optimize_places_with_distances(places_list: list[dict], start_city_name: str = None) -> dict:
        """
        Optimizes a list of places and calculates distances between each stop.
        
        Args:
            places_list (list[dict]): List of place dicts with 'lat', 'lon', 'name', 'owner'
        
        Returns:
            dict: {
                'optimized_places': cities in optimal order,
                'segments': distances between each pair of consecutive cities,
                'total_distance': total distance (round trip)
            }
        """
        if len(places_list) < 2:
            return {
                'optimized_places': places_list,
                'segments': [],
                'total_distance': 0.0
            }
        
        # Convertir en GeoPoints
        geopoints = [GeoPoint(p["lat"], p["lon"]) for p in places_list]
        
        # Optimiser l'ordre
        optimized_geopoints = TourOptimiszer.nearest_neighbor(geopoints)
        
        # STEP 5: Find complete places (dicts) in new order
        # We only have coordinates, so match with original places
        optimized_places = []
        for opt_gp in optimized_geopoints[:-1]:
            for place in places_list:
                if place["lat"] == opt_gp.lat and place["lon"] == opt_gp.lon and place not in optimized_places:
                    optimized_places.append(place)
                    break
        
        # Calculer les distances entre chaque segment
        segments = []
        total_dist = 0.0
        
        for i in range(len(optimized_places)):
            if i == 0:
                # First city: no previous distance
                segments.append({
                    'from': None,
                    'to': optimized_places[0]['name'],
                    'distance': 0.0
                })
            else:
                # Calculate distance between previous city and current city
                prev_gp = GeoPoint(optimized_places[i - 1]["lat"], optimized_places[i - 1]["lon"])
                curr_gp = GeoPoint(optimized_places[i]["lat"], optimized_places[i]["lon"])
                dist = DistanceCalculator.distance(prev_gp, curr_gp)
                total_dist += dist
                segments.append({
                    'from': optimized_places[i-1]['name'],
                    'to': optimized_places[i]['name'],
                    'distance': dist
                })

        # STEP 7: Distance for return trip (last city -> first city)
        last_gp = GeoPoint(optimized_places[-1]["lat"], optimized_places[-1]["lon"])
        first_gp = GeoPoint(optimized_places[0]["lat"], optimized_places[0]["lon"])
        dist_return = DistanceCalculator.distance(last_gp, first_gp)
        total_dist += dist_return
        segments.append({
            'from': optimized_places[-1]['name'],
            'to': optimized_places[0]['name'],
            'distance': dist_return,
            'is_return': True
        })
        
        return {
            'optimized_places': optimized_places,
            'segments': segments,
            'total_distance': total_dist
        }


