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

def target_compressive_strength(grade):
    """Calculate target compressive strength."""
    if grade == "M 10" or grade == "M 15":
        g = "M1"
    elif grade == "M 20" or grade == "M 25":
        g = "M2"
    else:
        g = "M3_5"
    return int(grade.replace("M ", '')) + (1.65 * GRADE_STANDARD_DEVIATION_TABLE.get(g, 0))

def water_cement_ratio(exposure):
    """Calculate water cement ratio."""
    exp = exposure.capitalize()
    return EXPOSURE_CONDITIONS_TABLE.get(exp, [0, 0])[1]

def max_water_content(slump, s_a, type_agg, admixture):
    """Calculate maximum water content."""
    s_a_str = str(int(s_a))  # Convert s_a to string
    n = (int(slump) - 50) / 25
    w_content = MAX_WATER_CONTENT_TABLE.get(s_a_str, 0)
    if type_agg == "sub-angular":
        w_content -= 10
    elif type_agg == "gravel":
        w_content -= 20
    elif type_agg == "rounded gravel":
        w_content -= 25
    if int(slump) > 50:
        w_content += (0.03 * n * w_content)
    if admixture == "Super Plasticizer":
        w_content -= w_content * 0.2
    elif admixture == "Plasticizer":
        w_content -= w_content * 0.1
    return w_content

def cement_content(exposure, w_c_r, w_c):
    """Calculate cement content."""
    exp = exposure.capitalize()
    min_c_c = EXPOSURE_CONDITIONS_TABLE.get(exp, [0, 0])[0]
    c_content = w_c / w_c_r
    return max(c_content, min_c_c)

def cement_flyAsh_content(exposure, w_c_r, w_content):
    """Calculate cement and fly ash content."""
    exp = exposure.capitalize()
    for a, b in EXPOSURE_CONDITIONS_TABLE.items():
        if a == exp:
            min_c_c = b[0]
    c_content = w_content / w_c_r
    t1 = c_content
    if c_content < min_c_c:
        c_content = min_c_c
        t1 = c_content
    c_content *= 1.10
    corrected_w_c_r = w_content / c_content
    flyA_content = c_content * 0.3
    t2 = c_content
    t2 -= flyA_content
    i = 0.25
    if t2 < 270:
        while True and i > 0:
            t2 = c_content
            flyA_content = c_content * i
            t2 -= flyA_content
            i -= 0.05
            if t2 >= 270:
                flya_percentage = int((i+0.05)*100)
                break
            elif i < 0:
                return None, None, None, None, None
    else:
        flya_percentage = int((i+0.05)*100)
    c_content = t2
    c_reduced = t1 - c_content
    return c_content, flyA_content, c_reduced, corrected_w_c_r, flya_percentage


