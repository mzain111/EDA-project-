import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from filters import load_and_clean_data, apply_filters, get_kpi_metrics
from charts import (
    pie_chart_stroke,
    histogram_age,
    line_chart_stroke_by_age,
    bar_chart_work_type,
    scatter_glucose_bmi,
    box_plot_age_glucose,
    heatmap_correlation,
    area_chart_bmi_category,
    count_plot_smoking,
    violin_plot_age_gender,
)

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Stroke EDA Dashboard — 70177766",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #F8F9FA; }
    .block-container { padding-top: 1.5rem; }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #2E86AB;
    }
    .kpi-value { font-size: 28px; font-weight: 700; color: #2E86AB; }
    .kpi-label { font-size: 12px; color: #666; margin-top: 4px; }
    .section-header {
        background: linear-gradient(90deg, #2E86AB, #1D3557);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        margin: 20px 0 12px 0;
        font-weight: 600;
        font-size: 16px;
    }
    .stMetric { background: white; border-radius: 8px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_and_clean_data(
        "data/healthcare-dataset-stroke-data.csv"
    )

df_raw = get_data()

# ═══════════════════════════════════════════════════════════════════
#  SIDEBAR — ALL FILTERS
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/brain.png",
        width=60
    )
    st.title("Dashboard Filters")
    st.caption("Student ID: 70177766")
    st.markdown("---")

    # 1 — Category Filter: Gender
    st.subheader("1. Gender Filter")
    gender_options = sorted(df_raw['gender'].unique().tolist())
    gender_filter = st.multiselect(
        "Select Gender",
        options=gender_options,
        default=gender_options,
        key="gender"
    )

    st.markdown("---")

    # 2 — Numerical Range Slider: Age
    st.subheader("2. Age Range")
    age_min = int(df_raw['age'].min())
    age_max = int(df_raw['age'].max())
    age_range = st.slider(
        "Select Age Range",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max),
        key="age_slider"
    )

    st.markdown("---")

    # 3 — Numerical Range Slider: Glucose
    st.subheader("3. Glucose Level Range")
    glc_min = float(df_raw['avg_glucose_level'].min())
    glc_max = float(df_raw['avg_glucose_level'].max())
    glucose_range = st.slider(
        "Select Glucose Range (mg/dL)",
        min_value=glc_min,
        max_value=glc_max,
        value=(glc_min, glc_max),
        key="glucose_slider"
    )

    st.markdown("---")

    # 4 — Multi-Select Filter: Work Type
    st.subheader("4. Work Type")
    work_options = sorted(df_raw['work_type'].unique().tolist())
    work_filter = st.multiselect(
        "Select Work Type(s)",
        options=work_options,
        default=work_options,
        key="work_type"
    )

    st.markdown("---")

    # 5 — Multi-Select Filter: Smoking Status
    st.subheader("5. Smoking Status")
    smoke_options = sorted(df_raw['smoking_status'].unique().tolist())
    smoke_filter = st.multiselect(
        "Select Smoking Status",
        options=smoke_options,
        default=smoke_options,
        key="smoking"
    )

    st.markdown("---")

    # 6 — Search / Text Filter
    st.subheader("6. Search / Text Filter")
    search_text = st.text_input(
        "Search (gender, work type, smoking, residence)",
        value="",
        placeholder="e.g. Male, Private, Urban...",
        key="search"
    )

    st.markdown("---")

    # 7 — Reset All Filters Button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state.gender        = gender_options
        st.session_state.age_slider    = (age_min, age_max)
        st.session_state.glucose_slider = (glc_min, glc_max)
        st.session_state.work_type     = work_options
        st.session_state.smoking       = smoke_options
        st.session_state.search        = ""
        st.rerun()

    st.markdown("---")
    st.caption("Instructor: Ali Hassan Sherazi")
    st.caption("Course: Exploratory Data Analysis")

# ── Apply all filters ─────────────────────────────────────────────
df = apply_filters(
    df_raw,
    gender_filter  = gender_filter,
    age_range      = age_range,
    glucose_range  = glucose_range,
    work_type_filter = work_filter,
    smoking_filter = smoke_filter,
    search_text    = search_text,
)

kpi = get_kpi_metrics(df)

# ═══════════════════════════════════════════════════════════════════
#  MAIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════

# Header
st.markdown("""
<div style='background:linear-gradient(135deg,#1D3557,#2E86AB);
            padding:24px 28px; border-radius:12px; margin-bottom:20px;'>
    <h1 style='color:white; margin:0; font-size:28px;'>
        🧠 Stroke Prediction — Data Visualization Dashboard
    </h1>
    <p style='color:#A8DADC; margin:6px 0 0 0; font-size:14px;'>
        Student ID: 70177766 &nbsp;|&nbsp;
        Dataset: Stroke Prediction (Kaggle) &nbsp;|&nbsp;
        Course: Exploratory Data Analysis &nbsp;|&nbsp;
        Instructor: Ali Hassan Sherazi
    </p>
</div>
""", unsafe_allow_html=True)

# Filter status
if len(df) < len(df_raw):
    st.info(
        f"🔍 Filters active — showing **{len(df):,}** of "
        f"**{len(df_raw):,}** total records."
    )
else:
    st.success(f"✅ Showing all **{len(df):,}** records — no filters applied.")

# ── KPI Cards ─────────────────────────────────────────────────────
st.markdown(
    "<div class='section-header'>📊 KPI Summary Cards</div>",
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
kpi_items = [
    (c1, kpi['total_records'],      "Total Patients"),
    (c2, kpi['stroke_cases'],       "Stroke Cases"),
    (c3, f"{kpi['stroke_rate']}%",  "Stroke Rate"),
    (c4, kpi['avg_age'],            "Avg Age"),
    (c5, kpi['avg_glucose'],        "Avg Glucose"),
    (c6, kpi['avg_bmi'],            "Avg BMI"),
    (c7, f"{kpi['hypertension_pct']}%", "Hypertension %"),
    (c8, f"{kpi['heart_disease_pct']}%","Heart Disease %"),
]
for col, val, label in kpi_items:
    with col:
        st.markdown(
            f"""<div class='kpi-card'>
                    <div class='kpi-value'>{val}</div>
                    <div class='kpi-label'>{label}</div>
                </div>""",
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  SECTION 1 — DISTRIBUTION ANALYSIS
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>📈 Section 1 — Distribution Analysis</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Chart 1 — Pie Chart: Stroke Distribution")
    st.write("Proportional breakdown of stroke vs no-stroke patients.")
    if len(df) > 0:
        st.pyplot(pie_chart_stroke(df))
    else:
        st.warning("No data available for current filters.")

with col2:
    st.subheader("Chart 2 — Histogram: Age Distribution")
    st.write("Frequency distribution of patient ages with mean and median lines.")
    if len(df) > 0:
        st.pyplot(histogram_age(df))
    else:
        st.warning("No data available for current filters.")

# ═══════════════════════════════════════════════════════════════════
#  SECTION 2 — TREND & COMPARISON ANALYSIS
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>📉 Section 2 — Trend & Comparison Analysis</div>",
    unsafe_allow_html=True
)

st.subheader("Chart 3 — Line Chart: Stroke Rate by Age Group")
st.write("How does stroke risk change as patients get older?")
if len(df) > 0:
    st.pyplot(line_chart_stroke_by_age(df))
else:
    st.warning("No data available for current filters.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Chart 4 — Bar Chart: Stroke by Work Type")
    st.write("Comparing stroke cases and rates across different work types.")
    if len(df) > 0:
        st.pyplot(bar_chart_work_type(df))
    else:
        st.warning("No data available for current filters.")

with col2:
    st.subheader("Chart 9 — Count Plot: Smoking vs Stroke")
    st.write("Frequency count of smoking status categories by stroke outcome.")
    if len(df) > 0:
        st.pyplot(count_plot_smoking(df))
    else:
        st.warning("No data available for current filters.")

# ═══════════════════════════════════════════════════════════════════
#  SECTION 3 — RELATIONSHIP ANALYSIS
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>🔗 Section 3 — Relationship Analysis</div>",
    unsafe_allow_html=True
)

st.subheader("Chart 5 — Scatter Plot: Glucose vs BMI")
st.write("Relationship between glucose levels and BMI, coloured by stroke outcome.")
if len(df) > 0:
    st.pyplot(scatter_glucose_bmi(df))
else:
    st.warning("No data available for current filters.")

st.subheader("Chart 6 — Box Plot: Age & Glucose by Stroke Status")
st.write("Spread, median, and outliers of age and glucose across stroke groups.")
if len(df) > 0:
    st.pyplot(box_plot_age_glucose(df))
else:
    st.warning("No data available for current filters.")

# ═══════════════════════════════════════════════════════════════════
#  SECTION 4 — ADVANCED ANALYSIS
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>🔬 Section 4 — Advanced Analysis</div>",
    unsafe_allow_html=True
)

st.subheader("Chart 7 — Heatmap: Feature Correlation Matrix")
st.write("Which features are most strongly correlated with stroke occurrence?")
if len(df) > 0:
    st.pyplot(heatmap_correlation(df))
else:
    st.warning("No data available for current filters.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Chart 8 — Area Chart: Patients by BMI Category")
    st.write("Cumulative patient distribution across BMI categories by stroke.")
    if len(df) > 0:
        st.pyplot(area_chart_bmi_category(df))
    else:
        st.warning("No data available for current filters.")

with col2:
    st.subheader("Chart 10 — Violin Plot: Age by Gender & Stroke")
    st.write("Distribution and probability density of age across gender and stroke.")
    if len(df) > 0:
        st.pyplot(violin_plot_age_gender(df))
    else:
        st.warning("No data available for current filters.")

# ═══════════════════════════════════════════════════════════════════
#  SECTION 5 — DATA TABLE
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>📋 Section 5 — Filtered Data Table</div>",
    unsafe_allow_html=True
)

st.write(f"Showing **{len(df):,}** rows matching current filters.")
display_cols = ['gender', 'age', 'age_group', 'hypertension',
                'heart_disease', 'ever_married', 'work_type',
                'residence_type', 'avg_glucose_level',
                'glucose_category', 'bmi', 'bmi_category',
                'smoking_status', 'stroke']
st.dataframe(
    df[display_cols].reset_index(drop=True),
    use_container_width=True,
    height=350
)

# Download filtered data button
csv = df[display_cols].to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name='stroke_filtered_data.csv',
    mime='text/csv',
)

# ── Key Findings ──────────────────────────────────────────────────
st.markdown(
    "<div class='section-header'>💡 Key Findings & Conclusion</div>",
    unsafe_allow_html=True
)

st.markdown(f"""
| # | Finding | Detail |
|---|---------|--------|
| 1 | **Severe Class Imbalance** | Only ~4.9% of patients had a stroke (249 out of 5,110) |
| 2 | **Age is #1 Risk Factor** | Stroke patients avg age ~68 vs non-stroke avg ~43 years |
| 3 | **High Glucose = Higher Risk** | Stroke patients show significantly higher glucose levels |
| 4 | **Hypertension Increases Risk** | {kpi['hypertension_pct']}% of current filtered patients have hypertension |
| 5 | **Heart Disease Increases Risk** | {kpi['heart_disease_pct']}% of current filtered patients have heart disease |
| 6 | **BMI has Moderate Link** | Obese patients show slightly higher stroke proportions |
| 7 | **Smoking has Some Effect** | Formerly smoked group shows elevated proportional stroke risk |
| 8 | **Self-employed at Higher Risk** | Self-employed work type shows elevated stroke rate |

### Conclusion
Age, glucose levels, hypertension, and heart disease are the most important
factors associated with stroke. The dataset is severely imbalanced (95% no-stroke)
which is a critical consideration for any future predictive modelling.
""")

st.success("✅ Dashboard Complete — Student ID: 70177766 | All 10 Charts | All 6 Filters")
st.caption(
    "Dataset: Stroke Prediction (Kaggle) | "
    "Tools: Python · Pandas · NumPy · Matplotlib · Seaborn · Streamlit"
)
