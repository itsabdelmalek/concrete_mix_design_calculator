#!/usr/bin/env python3
import unittest
from app import (
    target_compressive_strength,
    water_cement_ratio,
    max_water_content,
    cement_content,
)


class TestConcreteMixDesign(unittest.TestCase):
    def test_target_compressive_strength(self):
        """Test target compressive strength calculation for different grades."""
        self.assertEqual(target_compressive_strength("M 15"), 20.775)
        self.assertEqual(target_compressive_strength("M 20"), 26.6)
        self.assertEqual(target_compressive_strength("M 25"), 31.6)
        self.assertEqual(target_compressive_strength("M 30"), 38.25)
        self.assertEqual(target_compressive_strength("M 35"), 43.25)
        self.assertEqual(target_compressive_strength("M 40"), 48.25)
        self.assertEqual(target_compressive_strength("M 45"), 53.25)
        self.assertEqual(target_compressive_strength("M 50"), 58.25)

    def test_water_cement_ratio(self):
        """Test water cement ratio calculation for different exposure conditions."""
        self.assertEqual(water_cement_ratio("Mild"), 0.55)
        self.assertEqual(water_cement_ratio("Moderate"), 0.50)
        self.assertEqual(water_cement_ratio("Severe"), 0.45)
        self.assertEqual(water_cement_ratio("Very severe"), 0.45)
        self.assertEqual(water_cement_ratio("Extreme"), 0.40)

    def test_max_water_content(self):
        """Test maximum water content calculation with specific parameters."""
        result = max_water_content(150, 20, "sub-angular", "Plasticizer")
        # Adjusted expected result with a tolerance of 0.1
        expected_result = 177.4
        tolerance = 0.1
        self.assertAlmostEqual(result, expected_result, delta=tolerance)
    
    def test_cement_content(self):
        """Test cement content calculation for exposure and water/cement ratio."""
        result = cement_content("Moderate", 0.50, 150)
        expected_result = 300
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
