"""
test_algorithm_edge_cases.py — Edge cases and error handling tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.algorithm import TourOptimiszer, DistanceCalculator, GeoPoint


class TestAlgorithmEdgeCases(unittest.TestCase):

    def test_optimize_empty_list(self):
        """optimize_places_with_distances must handle empty list."""
        result = TourOptimiszer.optimize_places_with_distances([])
        
        self.assertEqual(result['optimized_places'], [])
        self.assertEqual(result['segments'], [])
        self.assertEqual(result['total_distance'], 0.0)

    def test_optimize_single_place(self):
        """optimize_places_with_distances must handle single place."""
        places = [{"name": "Paris", "lat": 48.8566, "lon": 2.3522, "owner": "user1"}]
        result = TourOptimiszer.optimize_places_with_distances(places)
        
        self.assertEqual(result['optimized_places'], places)
        self.assertEqual(result['total_distance'], 0.0)

    def test_optimize_two_places(self):
        """optimize_places_with_distances with exactly 2 places."""
        places = [
            {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "owner": "user1"},
            {"name": "Versailles", "lat": 48.8049, "lon": 2.1204, "owner": "user1"}
        ]
        result = TourOptimiszer.optimize_places_with_distances(places)
        
        # Should have 2 places
        self.assertEqual(len(result['optimized_places']), 2)
        
        # Should have 3 segments: start, Paris->Versailles, return
        self.assertGreaterEqual(len(result['segments']), 3)
        
        # Distance should be > 0
        self.assertGreater(result['total_distance'], 0)

    def test_optimize_with_start_city(self):
        """optimize_places_with_distances should start from specified city."""
        places = [
            {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "owner": "user1"},
            {"name": "Versailles", "lat": 48.8049, "lon": 2.1204, "owner": "user1"},
            {"name": "Lyon", "lat": 45.7640, "lon": 4.8357, "owner": "user1"}
        ]
        result = TourOptimiszer.optimize_places_with_distances(places, start_city_name="Versailles")
        
        # First city should be Versailles
        self.assertEqual(result['optimized_places'][0]['name'], "Versailles")

    def test_optimize_invalid_start_city(self):
        """If start_city not found, should default to first city."""
        places = [
            {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "owner": "user1"},
            {"name": "Versailles", "lat": 48.8049, "lon": 2.1204, "owner": "user1"}
        ]
        result = TourOptimiszer.optimize_places_with_distances(places, start_city_name="NonExistent")
        
        # Should still return optimized places (first city as default)
        self.assertEqual(len(result['optimized_places']), 2)

    def test_distance_same_point(self):
        """Distance between identical points should be zero (within tolerance)."""
        p1 = GeoPoint(48.8566, 2.3522)
        p2 = GeoPoint(48.8566, 2.3522)
        
        dist = DistanceCalculator.distance(p1, p2)
        self.assertLess(dist, 0.001)  # Within 1 meter

    def test_distance_zero_coordinates(self):
        """Distance from (0,0) to (0,0) should be zero."""
        p1 = GeoPoint(0, 0)
        p2 = GeoPoint(0, 0)
        
        dist = DistanceCalculator.distance(p1, p2)
        self.assertEqual(dist, 0.0)

    def test_distance_symmetry(self):
        """Distance A->B must equal B->A."""
        p1 = GeoPoint(48.8566, 2.3522)
        p2 = GeoPoint(45.7640, 4.8357)
        
        dist1 = DistanceCalculator.distance(p1, p2)
        dist2 = DistanceCalculator.distance(p2, p1)
        
        self.assertAlmostEqual(dist1, dist2, places=5)

    def test_nearest_neighbor_empty(self):
        """nearest_neighbor with empty list should return empty list."""
        result = TourOptimiszer.nearest_neighbor([])
        self.assertEqual(result, [])

    def test_nearest_neighbor_single_city(self):
        """nearest_neighbor with 1 city should return [city, city]."""
        city = GeoPoint(48.8566, 2.3522)
        result = TourOptimiszer.nearest_neighbor([city])
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].lat, result[1].lat)
        self.assertEqual(result[0].lon, result[1].lon)

    def test_two_opt_improves_or_equal(self):
        """2-opt should never make tour worse."""
        cities = [
            GeoPoint(48.8566, 2.3522),      # Paris
            GeoPoint(48.8049, 2.1204),      # Versailles
            GeoPoint(45.7640, 4.8357),      # Lyon
            GeoPoint(43.2965, 5.3698)       # Marseille
        ]
        
        # Get initial tour from nearest neighbor
        initial_tour = TourOptimiszer.nearest_neighbor(cities)
        initial_dist = TourOptimiszer.calculate_tour_distance(initial_tour)
        
        # Apply 2-opt
        optimized_tour = TourOptimiszer.two_opt(initial_tour[:-1])
        optimized_dist = TourOptimiszer.calculate_tour_distance(optimized_tour + [optimized_tour[0]])
        
        # 2-opt should not make it worse
        self.assertLessEqual(optimized_dist, initial_dist + 0.1)  # small tolerance for rounding

    def test_calculate_tour_distance_valid(self):
        """calculate_tour_distance should return positive value."""
        tour = [
            GeoPoint(48.8566, 2.3522),
            GeoPoint(45.7640, 4.8357),
            GeoPoint(48.8566, 2.3522)  # return to start
        ]
        
        dist = TourOptimiszer.calculate_tour_distance(tour)
        self.assertGreater(dist, 0)

    def test_split_by_hotels_preserves_all_places(self):
        """split_by_hotels must not lose any places."""
        places = [
            {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "owner": "user1"},
            {"name": "Versailles", "lat": 48.8049, "lon": 2.1204, "owner": "user1"},
            {"name": "Lyon", "lat": 45.7640, "lon": 4.8357, "owner": "user1"}
        ]
        
        result = TourOptimiszer.split_by_hotels(places, ["Paris"])
        
        # Count total places
        main_count = len(result["main_tour"])
        excursion_count = sum(len(ex) for ex in result["excursions"].values())
        total = main_count + excursion_count
        
        self.assertEqual(total, len(places))


if __name__ == "__main__":
    unittest.main()
