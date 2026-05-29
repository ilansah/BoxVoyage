"""
test_split_by_hotels.py — Tests for split_by_hotels function
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.algorithm import TourOptimiszer


class TestSplitByHotels(unittest.TestCase):

    def setUp(self):
        """Create test places around Paris region."""
        self.places = [
            {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "owner": "user1"},
            {"name": "Versailles", "lat": 48.8049, "lon": 2.1204, "owner": "user1"},
            {"name": "Fontainebleau", "lat": 48.4047, "lon": 2.6993, "owner": "user1"},
            {"name": "Lyon", "lat": 45.7640, "lon": 4.8357, "owner": "user1"},
            {"name": "Marseille", "lat": 43.2965, "lon": 5.3698, "owner": "user1"},
        ]

    def test_split_hotels_basic(self):
        """split_by_hotels must separate main tour and excursions."""
        result = TourOptimiszer.split_by_hotels(self.places, ["Paris"])

        # Paris should be in main_tour
        main_names = [p["name"] for p in result["main_tour"]]
        self.assertIn("Paris", main_names)

        # Versailles should be in Paris excursions (15km)
        self.assertIn("Versailles", [p["name"] for p in result["excursions"]["Paris"]])

    def test_split_hotels_distance_limit(self):
        """Cities beyond 60km should NOT be in excursions."""
        result = TourOptimiszer.split_by_hotels(self.places, ["Paris"], limit=60.0)

        # Versailles (15km) should be excursion
        excursion_names = [p["name"] for p in result["excursions"]["Paris"]]
        self.assertIn("Versailles", excursion_names)

        # Fontainebleau is close (50km), should be excursion
        self.assertIn("Fontainebleau", excursion_names)

        # Lyon (400km) should be in main_tour, NOT in excursions
        self.assertEqual(len(result["excursions"]["Paris"]), 2)

    def test_split_hotels_multiple_hotels(self):
        """Test with multiple hotels."""
        result = TourOptimiszer.split_by_hotels(self.places, ["Paris", "Lyon"])

        # Both hotels in main_tour
        main_names = [p["name"] for p in result["main_tour"]]
        self.assertIn("Paris", main_names)
        self.assertIn("Lyon", main_names)

        # Both hotels should have excursions key
        self.assertIn("Paris", result["excursions"])
        self.assertIn("Lyon", result["excursions"])

    def test_split_hotels_nearest_assignment(self):
        """City should be assigned to NEAREST hotel within limit."""
        # Versailles is closer to Paris (15km) than any other point
        result = TourOptimiszer.split_by_hotels(self.places, ["Paris", "Lyon"])

        # Versailles should be assigned to Paris (nearer)
        paris_excursions = [p["name"] for p in result["excursions"]["Paris"]]
        self.assertIn("Versailles", paris_excursions)

    def test_split_hotels_no_hotels(self):
        """If no hotel_names provided, all places should stay in main_tour."""
        result = TourOptimiszer.split_by_hotels(self.places, [])

        # All places in main_tour
        self.assertEqual(len(result["main_tour"]), len(self.places))

        # No excursions
        self.assertEqual(len(result["excursions"]), 0)

    def test_split_hotels_single_city(self):
        """Single city cannot be a hotel (no excursions possible)."""
        single_place = [{"name": "Paris", "lat": 48.8566, "lon": 2.3522, "owner": "user1"}]
        
        result = TourOptimiszer.split_by_hotels(single_place, ["Paris"])

        # Paris in main_tour, no excursions
        self.assertIn("Paris", [p["name"] for p in result["main_tour"]])
        self.assertEqual(len(result["excursions"]["Paris"]), 0)

    def test_split_hotels_custom_limit(self):
        """Test with custom distance limit."""
        # Fontainebleau is ~50km from Paris
        result_30 = TourOptimiszer.split_by_hotels(self.places, ["Paris"], limit=30.0)
        result_60 = TourOptimiszer.split_by_hotels(self.places, ["Paris"], limit=60.0)

        # At 30km: Fontainebleau NOT in excursions
        excursions_30 = [p["name"] for p in result_30["excursions"]["Paris"]]
        self.assertNotIn("Fontainebleau", excursions_30)

        # At 60km: Fontainebleau IS in excursions
        excursions_60 = [p["name"] for p in result_60["excursions"]["Paris"]]
        self.assertIn("Fontainebleau", excursions_60)


if __name__ == "__main__":
    unittest.main()
