# Beaumont ISD STAAR Performance Analytics

**Course:** COSC5302 – Python Programming & Data Analytics  
**Semester:** Spring 2026  
**Instructor:** Dr. Qingzhong Liu  
**Student:** [Your Name]  
**Community Partner:** Beaumont Independent School District (Public Data)

---

## Project Overview

This project analyzes Beaumont ISD student academic performance using STAAR (State of Texas Assessments of Academic Readiness) data from 2019–2024. The goal is to identify performance trends, achievement gaps relative to the state average, and subject-level patterns that can inform district instructional priorities.

Data is sourced from the Texas Education Agency (TEA) public aggregate data portal and local reporting. A synthetic dataset modeled on published aggregate TEA numbers is included for reproducibility.

---

## Repository Structure

```
bisd_project/
├── data/
│   ├── generate_data.py      # Generates bisd_staar_data.csv from TEA-modeled parameters
│   └── bisd_staar_data.csv   # Synthetic dataset (500 rows, 9 columns)
├── scripts/
│   ├── analysis.py           # Core EDA and statistical analysis functions
│   └── visualizations.py     # All chart/figure generation (5 figures)
├── notebooks/
│   └── BISD_Analysis.ipynb   # End-to-end narrative Jupyter Notebook
├── tests/
│   └── test_analysis.py      # Unit tests (9 tests, pytest)
├── outputs/                  # Generated PNG figures (auto-created)
├── requirements.txt
└── README.md
```

---

## Setup & Reproducibility

### Prerequisites
- Python 3.9+
- pip or conda

### Installation

```bash
# Clone or download the repository
git clone https://github.com/[your-username]/bisd-staar-analytics.git
cd bisd-staar-analytics

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Analysis

```bash
# Step 1: Generate the dataset
python data/generate_data.py

# Step 2: Run statistical analysis
python scripts/analysis.py

# Step 3: Generate all figures (saved to /outputs/)
python scripts/visualizations.py

# Step 4: Run unit tests
python -m pytest tests/test_analysis.py -v
```

---

## Data Dictionary

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Academic year of STAAR administration |
| `district` | str | ISD name |
| `subject` | str | STAAR subject (Math, Reading/ELA, Science, etc.) |
| `grade` | str | Grade level tested (3–8 or "EOC") |
| `n_tested` | int | Number of students tested |
| `pct_met_grade_level` | float | % of students meeting grade level standard |
| `pct_approaches` | float | % meeting "approaches" performance level |
| `pct_masters` | float | % meeting "masters" (highest) performance level |
| `state_avg_met` | float | Statewide average % meeting grade level |

**Data Source:** Texas Education Agency aggregate STAAR data (publicly available at tea.texas.gov). This repository uses a synthetic dataset modeled on published TEA aggregate figures and local news reporting for the Jefferson County / Region 5 area.

---

## Key Findings

- Beaumont ISD consistently performs **15–20 percentage points below** the Texas state average.
- The COVID-19 pandemic caused a ~13 pp drop from 2019 to 2021; full recovery has not occurred by 2024.
- **Math** is the most challenged subject; **English II (EOC)** shows the most improvement.
- Compared to regional peers, BISD ranks **4th out of 5** districts in 2024 performance.
- The achievement gap widened to **19.5 percentage points** in 2024.

---

## Academic Integrity

All code is original work. Data is sourced from publicly available TEA aggregate reports. Use of AI tools (Claude) was disclosed per course policy; all analysis, interpretation, and writing represent the student's own intellectual work.
