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


