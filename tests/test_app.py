#!/usr/bin/env python3
import unittest
from app import (
    target_compressive_strength,
    water_cement_ratio,
    max_water_content,
    cement_content,
    total_aggregate_volume,
    cement_flyAsh_content,
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

    def test_total_aggregate_volume(self):
        """Test calculation of total coarse and fine aggregate volume."""
        CA_vol, FA_vol = total_aggregate_volume("Zone 1", 20, 0.50, True)
        expected_CA_vol = 0.54
        expected_FA_vol = 0.46
        self.assertAlmostEqual(CA_vol, expected_CA_vol, places=2)
        self.assertAlmostEqual(FA_vol, expected_FA_vol, places=2)

    def test_cement_flyAsh_content(self):
        """Test cement_flyAsh_content function for moderate exposure condition."""
        c_content, flyA_content, c_reduced, corrected_w_c_r, flya_percentage = cement_flyAsh_content("Moderate", 0.50, 150)
        expected_c_content = 280
        expected_flyA_content = 50
        expected_c_reduced = 300 - 280
        expected_corrected_w_c_r = 150 / 330
        expected_flya_percentage = 15
        tolerance = 0.5
        self.assertAlmostEqual(c_content, expected_c_content, delta=tolerance)
        self.assertAlmostEqual(flyA_content, expected_flyA_content, delta=tolerance)
        self.assertAlmostEqual(c_reduced, expected_c_reduced, delta=tolerance)
        self.assertAlmostEqual(corrected_w_c_r, expected_corrected_w_c_r, delta=tolerance)
        self.assertAlmostEqual(flya_percentage, expected_flya_percentage, delta=tolerance)

if __name__ == "__main__":
    unittest.main()