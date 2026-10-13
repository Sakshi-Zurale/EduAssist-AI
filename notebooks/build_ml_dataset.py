import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("../Dataset/OULAD")
PROCESSED_DIR = Path("../data/processed")

print("=" * 70)
print("BUILDING LEAKAGE-SAFE ML DATASET")
print("=" * 70)

# ============================================================
# 1. LOAD DATA
# ============================================================

print("\nLoading datasets...")

assessments = pd.read_csv(DATA_DIR / "assessments.csv")
student_assessment = pd.read_csv(DATA_DIR / "studentAssessment.csv")
student_info = pd.read_csv(DATA_DIR / "studentInfo.csv")
student_vle = pd.read_csv(DATA_DIR / "studentVle.csv")

print("✓ Datasets loaded")


# ============================================================
# 2. PREPARE ASSESSMENT DATA
# ============================================================

print("\nPreparing assessment data...")

assessment_data = student_assessment.merge(
    assessments[
        [
            "id_assessment",
            "code_module",
            "code_presentation",
            "assessment_type",
            "date",
            "weight"
        ]
    ],
    on="id_assessment",
    how="left"
)

# Remove records without assessment date or score
assessment_data = assessment_data.dropna(
    subset=["date", "score"]
)

# Sort chronologically
assessment_data = assessment_data.sort_values(
    [
        "id_student",
        "code_module",
        "code_presentation",
        "date"
    ]
)

# Assessment number within each student + module + presentation
assessment_data["assessment_number"] = (
    assessment_data
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .cumcount() + 1
)

print("Valid assessment records:", len(assessment_data))


# ============================================================
# 3. SELECT STUDENTS WITH AT LEAST 3 ASSESSMENTS
# ============================================================

group_counts = (
    assessment_data
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .size()
    .reset_index(name="assessment_count")
)

eligible = group_counts[
    group_counts["assessment_count"] >= 3
]

print("Eligible student-module records:", len(eligible))


# ============================================================
# 4. GET FIRST TWO ASSESSMENTS
# ============================================================

early = assessment_data[
    assessment_data["assessment_number"] <= 2
].copy()

early_features = (
    early
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .agg(
        first_score=("score", "first"),
        second_score=("score", "last"),
        early_avg_score=("score", "mean"),
        early_min_score=("score", "min"),
        early_max_score=("score", "max"),
        early_assessment_count=("score", "count"),
        second_assessment_date=("date", "last")
    )
    .reset_index()
)

# Score trend
early_features["score_trend"] = (
    early_features["second_score"]
    - early_features["first_score"]
)

print(
    "Student-module records from first 2 assessments:",
    len(early_features)
)


# ============================================================
# 5. CALCULATE FUTURE PERFORMANCE TARGET
# ============================================================

future = assessment_data[
    assessment_data["assessment_number"] > 2
].copy()

future_target = (
    future
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .agg(
        future_average_score=("score", "mean"),
        future_min_score=("score", "min"),
        future_max_score=("score", "max"),
        future_assessment_count=("score", "count")
    )
    .reset_index()
)

print(
    "Records with future performance:",
    len(future_target)
)


# ============================================================
# 6. MERGE EARLY FEATURES + TARGET
# ============================================================

ml_data = early_features.merge(
    future_target,
    on=[
        "id_student",
        "code_module",
        "code_presentation"
    ],
    how="inner"
)

print(
    "After merging early features and target:",
    len(ml_data)
)


# ============================================================
# 7. ADD STUDENT PROFILE
# ============================================================

profile_columns = [
    "id_student",
    "code_module",
    "code_presentation",
    "gender",
    "region",
    "highest_education",
    "imd_band",
    "age_band",
    "num_of_prev_attempts",
    "studied_credits",
    "disability"
]

profile = student_info[profile_columns].copy()

ml_data = ml_data.merge(
    profile,
    on=[
        "id_student",
        "code_module",
        "code_presentation"
    ],
    how="left"
)

print("✓ Student profile added")


# ============================================================
# 8. TIME-AWARE VLE ENGAGEMENT
# ============================================================

print("\nCalculating engagement before second assessment...")

# Keep only columns needed
vle = student_vle[
    [
        "code_module",
        "code_presentation",
        "id_student",
        "date",
        "id_site",
        "sum_click"
    ]
].copy()

# Merge cutoff date
vle = vle.merge(
    early_features[
        [
            "id_student",
            "code_module",
            "code_presentation",
            "second_assessment_date"
        ]
    ],
    on=[
        "id_student",
        "code_module",
        "code_presentation"
    ],
    how="inner"
)

# IMPORTANT:
# Only engagement on or before the second assessment
vle = vle[
    vle["date"] <= vle["second_assessment_date"]
]

engagement = (
    vle
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .agg(
        clicks_before_cutoff=("sum_click", "sum"),
        active_days_before_cutoff=("date", "nunique"),
        unique_resources_before_cutoff=("id_site", "nunique"),
        vle_records_before_cutoff=("sum_click", "count")
    )
    .reset_index()
)

# Average daily clicks
engagement["average_daily_clicks_before_cutoff"] = (
    engagement["clicks_before_cutoff"]
    / engagement["active_days_before_cutoff"]
)

print(
    "Student-module records with pre-cutoff engagement:",
    len(engagement)
)


# ============================================================
# 9. MERGE ENGAGEMENT
# ============================================================

ml_data = ml_data.merge(
    engagement,
    on=[
        "id_student",
        "code_module",
        "code_presentation"
    ],
    how="left"
)

# Students without VLE activity receive zero
engagement_columns = [
    "clicks_before_cutoff",
    "active_days_before_cutoff",
    "unique_resources_before_cutoff",
    "vle_records_before_cutoff",
    "average_daily_clicks_before_cutoff"
]

for column in engagement_columns:
    ml_data[column] = ml_data[column].fillna(0)


# ============================================================
# 10. CREATE FUTURE PERFORMANCE CATEGORY
# ============================================================

def performance_category(score):
    if score < 50:
        return "Low"
    elif score < 65:
        return "Needs Improvement"
    elif score < 80:
        return "Good"
    else:
        return "Excellent"


ml_data["future_performance_category"] = (
    ml_data["future_average_score"]
    .apply(performance_category)
)


# ============================================================
# 11. CREATE FUTURE RISK LEVEL
# ============================================================

def risk_level(score):
    if score < 50:
        return "High"
    elif score < 65:
        return "Medium"
    else:
        return "Low"


ml_data["future_risk_level"] = (
    ml_data["future_average_score"]
    .apply(risk_level)
)


# ============================================================
# 12. REMOVE UNNECESSARY COLUMNS
# ============================================================

# We do not use:
# - final_result
# - full-course average score
# - full-course engagement
# - future assessment scores as input features

# id_student is retained for traceability,
# but will NOT be used as an ML feature.

# ============================================================
# 13. SAVE DATASET
# ============================================================

output_path = (
    PROCESSED_DIR /
    "eduassist_ml_dataset.csv"
)

ml_data.to_csv(
    output_path,
    index=False
)


# ============================================================
# 14. SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("ML DATASET CREATED")
print("=" * 70)

print("\nShape:")
print(ml_data.shape)

print("\nColumns:")
for column in ml_data.columns:
    print("-", column)

print("\nFuture performance statistics:")
print(
    ml_data["future_average_score"].describe()
)

print("\nFuture performance categories:")
print(
    ml_data["future_performance_category"]
    .value_counts()
)

print("\nFuture risk levels:")
print(
    ml_data["future_risk_level"]
    .value_counts()
)

print("\nMissing values:")
print(
    ml_data.isnull().sum()
    [ml_data.isnull().sum() > 0]
)

print("\nSaved to:")
print(output_path)

print("\n" + "=" * 70)
print("LEAKAGE-SAFE ML DATASET BUILD COMPLETED")
print("=" * 70)
