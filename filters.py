import pandas as pd
import numpy as np


def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """Load and clean the stroke dataset."""
    df = pd.read_csv(filepath)

    # Standardise column names
    df.columns = df.columns.str.strip().str.lower()

    # Fill missing BMI with median
    df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
    df['bmi'].fillna(df['bmi'].median(), inplace=True)

    # Remove 1 row where gender = 'Other'
    df = df[df['gender'] != 'Other'].copy()

    # Clean age
    df['age'] = pd.to_numeric(df['age'], errors='coerce')

    # Age group column
    bins   = [0, 18, 35, 50, 65, 120]
    labels = ['0-18', '19-35', '36-50', '51-65', '65+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)

    # Glucose category
    df['glucose_category'] = pd.cut(
        df['avg_glucose_level'],
        bins=[0, 70, 100, 125, 500],
        labels=['Low', 'Normal', 'Pre-diabetic', 'Diabetic']
    )

    # BMI category
    df['bmi_category'] = pd.cut(
        df['bmi'],
        bins=[0, 18.5, 25, 30, 100],
        labels=['Underweight', 'Normal', 'Overweight', 'Obese']
    )

    return df


def apply_filters(df: pd.DataFrame,
                  gender_filter: list,
                  age_range: tuple,
                  glucose_range: tuple,
                  work_type_filter: list,
                  smoking_filter: list,
                  search_text: str) -> pd.DataFrame:
    """Apply all sidebar filters and return filtered dataframe."""
    filtered = df.copy()

    # Gender filter
    if gender_filter:
        filtered = filtered[filtered['gender'].isin(gender_filter)]

    # Age range slider
    filtered = filtered[
        (filtered['age'] >= age_range[0]) &
        (filtered['age'] <= age_range[1])
    ]

    # Glucose range slider
    filtered = filtered[
        (filtered['avg_glucose_level'] >= glucose_range[0]) &
        (filtered['avg_glucose_level'] <= glucose_range[1])
    ]

    # Work type multi-select
    if work_type_filter:
        filtered = filtered[filtered['work_type'].isin(work_type_filter)]

    # Smoking status multi-select
    if smoking_filter:
        filtered = filtered[filtered['smoking_status'].isin(smoking_filter)]

    # Search / text filter on work_type and smoking_status columns
    if search_text.strip():
        mask = (
            filtered['gender'].str.contains(search_text, case=False, na=False) |
            filtered['work_type'].str.contains(search_text, case=False, na=False) |
            filtered['smoking_status'].str.contains(search_text, case=False, na=False) |
            filtered['residence_type'].str.contains(search_text, case=False, na=False)
        )
        filtered = filtered[mask]

    return filtered


def get_kpi_metrics(df: pd.DataFrame) -> dict:
    """Return dictionary of KPI summary values."""
    return {
        'total_records':   len(df),
        'stroke_cases':    int(df['stroke'].sum()),
        'stroke_rate':     round(df['stroke'].mean() * 100, 2),
        'avg_age':         round(df['age'].mean(), 1),
        'avg_glucose':     round(df['avg_glucose_level'].mean(), 1),
        'avg_bmi':         round(df['bmi'].mean(), 1),
        'hypertension_pct': round(df['hypertension'].mean() * 100, 1),
        'heart_disease_pct': round(df['heart_disease'].mean() * 100, 1),
    }
