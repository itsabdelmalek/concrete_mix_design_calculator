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

def total_aggregate_volume(zone, s_a, w_c_r, pumping):
    """Calculate volume of coarse and fine aggregate."""
    s_a_str = str(int(s_a))  # Convert s_a to string
    i = {"Zone 4": 0, "Zone 3": 1, "Zone 2": 2, "Zone 1": 3}.get(zone, 0)
    CA_vol = COARSE_AGGREGATE_VOLUME_TABLE.get(s_a_str, [])[i]
    if w_c_r > 0.5:
        CA_vol -= 0.01 * ((w_c_r - 0.5) / 0.05)
    else:
        CA_vol += 0.01 * ((0.5 - w_c_r) / 0.05)
    if pumping:
        CA_vol *= 0.9
    FA_vol = 1 - CA_vol
    return CA_vol, FA_vol

# Define route for the index page
@app.route('/')
def index():
    return render_template('index.html')


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

def total_aggregate_volume(zone, s_a, w_c_r, pumping):
    """Calculate volume of coarse and fine aggregate."""
    s_a_str = str(int(s_a))  # Convert s_a to string
    i = {"Zone 4": 0, "Zone 3": 1, "Zone 2": 2, "Zone 1": 3}.get(zone, 0)
    CA_vol = COARSE_AGGREGATE_VOLUME_TABLE.get(s_a_str, [])[i]
    if w_c_r > 0.5:
        CA_vol -= 0.01 * ((w_c_r - 0.5) / 0.05)
    else:
        CA_vol += 0.01 * ((0.5 - w_c_r) / 0.05)
    if pumping:
        CA_vol *= 0.9
    FA_vol = 1 - CA_vol
    return CA_vol, FA_vol

# Define route for the index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Extract user inputs from the index page
    grade = request.form['grade']
    additions_type = request.form['additions_type']
    max_aggregate_size = float(request.form['max_aggregate_size'])
    slump = float(request.form['slump'])
    exposure_conditions = request.form['exposure_conditions']
    pouring_method = request.form['pouring_method']
    type_agg = request.form['type_agg']
    admixture = request.form['admixture']
    sp_cement = float(request.form['sp_cement'])
    sp_coarse_agg = float(request.form['sp_coarse_agg'])
    sp_fine_agg = float(request.form['sp_fine_agg'])
    sp_admixture = float(request.form['sp_admixture'])
    ca_water_absorption = float(request.form['ca_water_absorption'])
    fa_water_absorption = float(request.form['fa_water_absorption'])
    fa_zone = request.form['fa_zone']
    ca_surface_moisture = float(request.form['ca_surface_moisture'])
    fa_surface_moisture = float(request.form['fa_surface_moisture'])

    w_c_r = water_cement_ratio(exposure_conditions)
    w_content = max_water_content(slump, max_aggregate_size, type_agg, admixture)
    cement_c = cement_content(exposure_conditions, w_c_r, w_content)
    cement_fa_c, fly_ash_c, c_reduced, corrected_w_c_r, flya_percentage = cement_flyAsh_content(exposure_conditions, w_c_r, w_content)
    target_strength = target_compressive_strength(grade)
    CA_vol, FA_vol = total_aggregate_volume(fa_zone, max_aggregate_size, w_c_r, pouring_method == 'yes')

    if additions_type == 'Fly ash':
        sp_fly_ash = float(request.form['sp_fly_ash'])
        c_vol = (cement_fa_c / sp_cement) * 0.001
        fly_ash_vol = (fly_ash_c / sp_fly_ash) * 0.001
        w_vol = w_content * 0.001
        admixture_mass = cement_fa_c * 0.012
        admixture_volume = (admixture_mass / sp_admixture) * 0.001
        total_agg_vol = (1 - (c_vol + fly_ash_vol + w_vol + admixture_volume))
        FA_mass = total_agg_vol * FA_vol * sp_fine_agg * 1000
        CA_mass = total_agg_vol * CA_vol * sp_coarse_agg * 1000
        mix_proportions = {
            'Cement': round(cement_fa_c, 1),
            'Fly ash': round(fly_ash_c, 1),
            'Water': round(w_content, 1),
            'Fine aggregate': round(FA_mass, 1),
            'Coarse aggregate': round(CA_mass, 1),
            'Admixture': round(admixture_mass, 2),
            'Water cement ratio': round(corrected_w_c_r, 2)
        }
        output = {
            'target_strength': round(target_strength, 2),
            'volume_coarse_aggregate': round(CA_vol, 2),
            'volume_fine_aggregate': round(FA_vol, 2),
            'volume_cement': round(c_vol, 2),
            'volume_fly_ash': round(fly_ash_vol, 2),
            'fly_ash_percentage': flya_percentage,
            'volume_water': round(w_vol, 2),
            'cement_reduced': round(c_reduced, 2),
            'volume_admix': round(admixture_volume, 3),
            'volume_total_aggregate': round(total_agg_vol, 2),
            'mix_proportions': mix_proportions
        }


