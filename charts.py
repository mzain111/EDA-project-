import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── Consistent colour palette ─────────────────────────────────────
PRIMARY   = '#2E86AB'
SECONDARY = '#E84855'
ACCENT    = '#3BB273'
NEUTRAL   = '#A8DADC'
DARK      = '#1D3557'
PALETTE   = [PRIMARY, SECONDARY, ACCENT, NEUTRAL, DARK,
             '#F4A261', '#E76F51', '#264653', '#2A9D8F', '#E9C46A']

sns.set_theme(style='whitegrid', palette=PALETTE)
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'figure.facecolor': 'white',
    'axes.facecolor': '#F8F9FA',
})


# 1 ── Pie Chart ───────────────────────────────────────────────────
def pie_chart_stroke(df: pd.DataFrame):
    """Pie chart — stroke vs no-stroke distribution."""
    counts = df['stroke'].value_counts()
    labels = ['No Stroke', 'Stroke']
    colors = [PRIMARY, SECONDARY]
    explode = (0, 0.08)

    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts, autotexts = ax.pie(
        counts.values, labels=labels, autopct='%1.1f%%',
        colors=colors, explode=explode, startangle=140,
        textprops={'fontsize': 12}
    )
    for at in autotexts:
        at.set_fontweight('bold')
    ax.set_title('Stroke vs No-Stroke Distribution', fontsize=13,
                 fontweight='bold', pad=15)
    plt.tight_layout()
    return fig


# 2 ── Histogram ───────────────────────────────────────────────────
def histogram_age(df: pd.DataFrame):
    """Histogram — age frequency distribution."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df['age'], bins=30, color=PRIMARY,
            edgecolor='white', linewidth=0.8)
    ax.axvline(df['age'].mean(), color=SECONDARY, linestyle='--',
               linewidth=2, label=f"Mean: {df['age'].mean():.1f}")
    ax.axvline(df['age'].median(), color=ACCENT, linestyle='--',
               linewidth=2, label=f"Median: {df['age'].median():.1f}")
    ax.set_title('Age Frequency Distribution', fontsize=13, fontweight='bold')
    ax.set_xlabel('Age (years)')
    ax.set_ylabel('Number of Patients')
    ax.legend()
    plt.tight_layout()
    return fig


# 3 ── Line Chart ──────────────────────────────────────────────────
def line_chart_stroke_by_age(df: pd.DataFrame):
    """Line chart — stroke rate by age group."""
    age_stroke = (
        df.groupby('age_group', observed=True)['stroke']
        .mean()
        .reset_index()
    )
    age_stroke['stroke_rate'] = (age_stroke['stroke'] * 100).round(2)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(age_stroke['age_group'].astype(str),
            age_stroke['stroke_rate'],
            marker='o', color=PRIMARY, linewidth=2.5,
            markersize=8, markerfacecolor=SECONDARY)
    ax.fill_between(age_stroke['age_group'].astype(str),
                    age_stroke['stroke_rate'], alpha=0.15, color=PRIMARY)
    for i, row in age_stroke.iterrows():
        ax.annotate(f"{row['stroke_rate']}%",
                    (str(row['age_group']), row['stroke_rate']),
                    textcoords='offset points', xytext=(0, 10),
                    ha='center', fontsize=10, fontweight='bold')
    ax.set_title('Stroke Rate by Age Group', fontsize=13, fontweight='bold')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Stroke Rate (%)')
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    return fig


# 4 ── Bar Chart ───────────────────────────────────────────────────
def bar_chart_work_type(df: pd.DataFrame):
    """Bar chart — stroke count by work type."""
    work_stroke = (
        df.groupby('work_type')['stroke']
        .agg(['sum', 'count'])
        .reset_index()
    )
    work_stroke.columns = ['work_type', 'stroke_cases', 'total']
    work_stroke['stroke_rate'] = (
        work_stroke['stroke_cases'] / work_stroke['total'] * 100
    ).round(2)
    work_stroke = work_stroke.sort_values('stroke_cases', ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(work_stroke['work_type'], work_stroke['stroke_cases'],
                  color=PALETTE[:len(work_stroke)], edgecolor='white',
                  linewidth=0.8)
    for bar, rate in zip(bars, work_stroke['stroke_rate']):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1,
                f"{rate}%", ha='center', va='bottom',
                fontsize=10, fontweight='bold')
    ax.set_title('Stroke Cases by Work Type', fontsize=13, fontweight='bold')
    ax.set_xlabel('Work Type')
    ax.set_ylabel('Number of Stroke Cases')
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    return fig


# 5 ── Scatter Plot ────────────────────────────────────────────────
def scatter_glucose_bmi(df: pd.DataFrame):
    """Scatter plot — glucose level vs BMI coloured by stroke."""
    fig, ax = plt.subplots(figsize=(9, 6))
    colors = df['stroke'].map({0: PRIMARY, 1: SECONDARY})
    ax.scatter(df['avg_glucose_level'], df['bmi'],
               c=colors, alpha=0.5, s=20, edgecolors='none')
    legend_handles = [
        mpatches.Patch(color=PRIMARY,    label='No Stroke'),
        mpatches.Patch(color=SECONDARY,  label='Stroke'),
    ]
    ax.legend(handles=legend_handles, fontsize=11)
    ax.set_title('Glucose Level vs BMI (coloured by Stroke)',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Average Glucose Level (mg/dL)')
    ax.set_ylabel('BMI')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


# 6 ── Box Plot ────────────────────────────────────────────────────
def box_plot_age_glucose(df: pd.DataFrame):
    """Box plots — age and glucose by stroke status."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.boxplot(x='stroke', y='age', data=df,
                palette=[PRIMARY, SECONDARY], ax=axes[0])
    axes[0].set_xticklabels(['No Stroke', 'Stroke'])
    axes[0].set_title('Age Distribution by Stroke Status',
                      fontsize=13, fontweight='bold')
    axes[0].set_xlabel('')
    axes[0].set_ylabel('Age (years)')

    sns.boxplot(x='stroke', y='avg_glucose_level', data=df,
                palette=[PRIMARY, SECONDARY], ax=axes[1])
    axes[1].set_xticklabels(['No Stroke', 'Stroke'])
    axes[1].set_title('Glucose Level by Stroke Status',
                      fontsize=13, fontweight='bold')
    axes[1].set_xlabel('')
    axes[1].set_ylabel('Avg Glucose Level (mg/dL)')

    plt.tight_layout()
    return fig


# 7 ── Heatmap ─────────────────────────────────────────────────────
def heatmap_correlation(df: pd.DataFrame):
    """Heatmap — correlation matrix of all numeric features."""
    df_enc = df.copy()
    df_enc['gender']         = df_enc['gender'].map({'Male': 1, 'Female': 0})
    df_enc['ever_married']   = df_enc['ever_married'].map({'Yes': 1, 'No': 0})
    df_enc['residence_type'] = df_enc['residence_type'].map({'Urban': 1, 'Rural': 0})
    df_enc['work_type']      = df_enc['work_type'].astype('category').cat.codes
    df_enc['smoking_status'] = df_enc['smoking_status'].astype('category').cat.codes

    cols = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level',
            'bmi', 'stroke', 'gender', 'ever_married', 'work_type',
            'residence_type', 'smoking_status']
    corr = df_enc[cols].corr()

    fig, ax = plt.subplots(figsize=(11, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
                cmap='coolwarm', linewidths=0.5,
                square=True, ax=ax,
                cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Heatmap — All Features',
                 fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    return fig


# 8 ── Area Chart ──────────────────────────────────────────────────
def area_chart_bmi_category(df: pd.DataFrame):
    """Area chart — cumulative patient count by BMI category and stroke."""
    bmi_data = (
        df.groupby(['bmi_category', 'stroke'], observed=True)
        .size()
        .reset_index(name='count')
    )
    bmi_pivot = bmi_data.pivot(index='bmi_category',
                                columns='stroke',
                                values='count').fillna(0)
    bmi_pivot.columns = ['No Stroke', 'Stroke']
    bmi_pivot = bmi_pivot.loc[['Underweight', 'Normal',
                                'Overweight', 'Obese']]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.stackplot(bmi_pivot.index,
                 bmi_pivot['No Stroke'],
                 bmi_pivot['Stroke'],
                 labels=['No Stroke', 'Stroke'],
                 colors=[PRIMARY, SECONDARY], alpha=0.85)
    ax.set_title('Patient Count by BMI Category (Area Chart)',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('BMI Category')
    ax.set_ylabel('Number of Patients')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


# 9 ── Count Plot ──────────────────────────────────────────────────
def count_plot_smoking(df: pd.DataFrame):
    """Count plot — smoking status frequency by stroke outcome."""
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.countplot(x='smoking_status', hue='stroke', data=df,
                  palette=[PRIMARY, SECONDARY], ax=ax)
    ax.set_title('Smoking Status vs Stroke Outcome',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Smoking Status')
    ax.set_ylabel('Number of Patients')
    handles = [
        mpatches.Patch(color=PRIMARY,   label='No Stroke'),
        mpatches.Patch(color=SECONDARY, label='Stroke'),
    ]
    ax.legend(handles=handles)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    return fig


# 10 ── Violin Plot ────────────────────────────────────────────────
def violin_plot_age_gender(df: pd.DataFrame):
    """Violin plot — age distribution by gender and stroke status."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(x='gender', y='age', hue='stroke',
                   data=df, split=True,
                   palette=[PRIMARY, SECONDARY], ax=ax,
                   inner='quartile')
    ax.set_title('Age Distribution by Gender & Stroke (Violin Plot)',
                 fontsize=13, fontweight='bold')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Age (years)')
    handles = [
        mpatches.Patch(color=PRIMARY,   label='No Stroke'),
        mpatches.Patch(color=SECONDARY, label='Stroke'),
    ]
    ax.legend(handles=handles, title='Stroke Status')
    plt.tight_layout()
    return fig
