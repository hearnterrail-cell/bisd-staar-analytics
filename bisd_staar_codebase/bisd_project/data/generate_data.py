"""
generate_data.py
Generates synthetic Beaumont ISD STAAR performance dataset
modeled on publicly reported TEA aggregate data (2019–2024).
Run once to produce bisd_staar_data.csv in this directory.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# ── Subjects and grades tested ────────────────────────────────────────────────
subjects = {
    "Math":         [3, 4, 5, 6, 7, 8],
    "Reading/ELA":  [3, 4, 5, 6, 7, 8],
    "Science":      [5, 8],
    "Social Studies":[8],
    "Algebra I":    ["EOC"],
    "English I":    ["EOC"],
    "English II":   ["EOC"],
    "Biology":      ["EOC"],
    "U.S. History": ["EOC"],
}

# Base "met grade level" rates (%) modeled on TEA/local news reports
# Structure: subject -> {year: statewide_approx, bisd_approx}
# BISD consistently runs 15–25 pts below state average
base_rates = {
    # (state_avg, bisd_avg) by year – applied per grade with ±5 noise
    2019: {"state": 72, "bisd": 55},
    2020: {"state": 0,  "bisd": 0},   # COVID – no STAAR administered
    2021: {"state": 58, "bisd": 42},  # recovery year
    2022: {"state": 63, "bisd": 47},
    2023: {"state": 66, "bisd": 49},
    2024: {"state": 61, "bisd": 43},  # new redesigned test / AI grading
}

subject_modifier = {
    "Math":          0,
    "Reading/ELA":   3,
    "Science":      -5,
    "Social Studies":-3,
    "Algebra I":    -2,
    "English I":     2,
    "English II":    5,
    "Biology":       0,
    "U.S. History":  4,
}

years = [2019, 2021, 2022, 2023, 2024]
districts = ["Beaumont ISD", "Nederland ISD", "Port Arthur ISD",
             "Hamshire-Fannett ISD", "Hardin-Jefferson ISD"]

dist_modifier = {
    "Beaumont ISD":       0,
    "Nederland ISD":     20,
    "Port Arthur ISD":   -5,
    "Hamshire-Fannett ISD": 22,
    "Hardin-Jefferson ISD": 12,
}

rows = []
for year in years:
    for subject, grades in subjects.items():
        for grade in grades:
            for district in districts:
                bisd_base = base_rates[year]["bisd"] + subject_modifier[subject]
                state_base = base_rates[year]["state"] + subject_modifier[subject]
                bisd_met   = np.clip(bisd_base  + dist_modifier[district] + np.random.randint(-4, 5), 5, 98)
                state_met  = np.clip(state_base + np.random.randint(-3, 4), 5, 98)
                n_tested   = int(np.random.normal(850 if district=="Beaumont ISD" else 300, 80))
                n_tested   = max(n_tested, 30)
                rows.append({
                    "year": year,
                    "district": district,
                    "subject": subject,
                    "grade": str(grade),
                    "n_tested": n_tested,
                    "pct_met_grade_level": round(bisd_met, 1),
                    "pct_approaches": round(bisd_met + np.random.randint(5, 12), 1),
                    "pct_masters": round(bisd_met - np.random.randint(10, 20), 1),
                    "state_avg_met": round(state_met, 1),
                })

df = pd.DataFrame(rows)
df["pct_masters"] = df["pct_masters"].clip(lower=2)
df["pct_approaches"] = df["pct_approaches"].clip(upper=99)
df.to_csv("bisd_staar_data.csv", index=False)
print(f"Generated {len(df)} rows → bisd_staar_data.csv")
print(df.head())
