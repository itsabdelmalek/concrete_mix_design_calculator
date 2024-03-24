#!/usr/bin/env python3
import unittest
from app import (
    target_compressive_strength,
    water_cement_ratio,
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

if __name__ == "__main__":
    unittest.main()
