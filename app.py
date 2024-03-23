#!/usr/bin/env python3
"""Simple flask API for concrete mix design."""

from flask import Flask

app = Flask(__name__)

# ACI | "Exposure conditions": [Minimum cement content in kg/m^3, Maximum water to cement ratio]
EXPOSURE_CONDITIONS_TABLE = {
    "Mild": [300, 0.55],
    "Moderate": [300, 0.50],
    "Severe": [320, 0.45],
    "Very severe": [340, 0.45],
    "Extreme": [360, 0.40]
}

# ACI | "Grade": Assumed Standard Deviation
GRADE_STANDARD_DEVIATION_TABLE = {
    "M1": 3.5,
    "M2": 4.0,
    "M3_5": 5.0
}

# ACI | "Nominal Maximum Size Of Aggregate in mm": Maximum Water content in kg
MAX_WATER_CONTENT_TABLE = {"10": 208, "20": 186, "40": 165}

# ACI | "Nominal Maximum Size Of Aggregate in mm": (vol of coarse aggregates)[Zone 4, Zone 3, Zone 2, Zone 1]
COARSE_AGGREGATE_VOLUME_TABLE = {
    "10": [0.50, 0.48, 0.46, 0.44],
    "20": [0.66, 0.64, 0.62, 0.60],
    "40": [0.75, 0.73, 0.71, 0.69]
}


