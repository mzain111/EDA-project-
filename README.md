# Stroke Prediction — Data Visualization Dashboard

**Student ID:** 70177766
**Course:** Exploratory Data Analysis
**Instructor:** Ali Hassan Sherazi
**Submission Date:** 05-June-2026

---

## Project Overview
A fully functional, professional-grade data visualization dashboard
built on the Stroke Prediction dataset (5,110 patients, 12 features).
The dashboard includes 10 chart types, 6 interactive filters, KPI cards,
and a filtered data table with CSV download.

---

## Dataset
- **File:** `data/healthcare-dataset-stroke-data.csv`
- **Source:** Kaggle — Stroke Prediction Dataset
- **Records:** 5,110 patients | **Features:** 12 columns

---

## Project Structure
```
dashboard_project/
├── data/
│   └── healthcare-dataset-stroke-data.csv
├── notebooks/
│   └── analysis.ipynb
├── app.py          ← Main dashboard
├── charts.py       ← All 10 chart functions
├── filters.py      ← Data loading, cleaning, filter logic
├── requirements.txt
└── README.md
```

---

## How to Install & Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run the dashboard
```bash
streamlit run app.py
```

### Step 3 — Open in browser
Go to: `http://localhost:8501`

---

## Charts Included (All 10 Required)
1. Pie Chart — Stroke vs No-Stroke distribution
2. Histogram — Age frequency distribution
3. Line Chart — Stroke rate by age group
4. Bar Chart — Stroke cases by work type
5. Scatter Plot — Glucose vs BMI coloured by stroke
6. Box Plot — Age and glucose by stroke status
7. Heatmap — Feature correlation matrix
8. Area Chart — Patients by BMI category
9. Count Plot — Smoking status vs stroke
10. Violin Plot — Age distribution by gender and stroke

---

## Filters Included (All 6 Required)
1. Gender Filter (multi-select)
2. Age Range Slider (numerical)
3. Glucose Level Range Slider (numerical)
4. Work Type Filter (multi-select)
5. Smoking Status Filter (multi-select)
6. Search / Text Filter (keyword search)
7. Reset All Filters Button

---

## Key Insights
- Only 4.9% of patients had a stroke — severe class imbalance
- Age is the strongest risk factor (stroke avg ~68 vs non-stroke ~43)
- High glucose levels strongly linked to stroke risk
- Hypertension and heart disease increase stroke probability
- Larger companies provide more mental health benefits

---

## Tools & Libraries
| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Pandas | Data loading, cleaning, filtering |
| NumPy | Numerical operations |
| Matplotlib | Chart creation |
| Seaborn | Statistical visualizations |
| Streamlit | Interactive dashboard frontend |
