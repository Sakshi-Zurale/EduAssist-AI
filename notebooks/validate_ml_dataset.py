import pandas as pd
from pathlib import Path

DATA_PATH = Path("../data/processed/eduassist_ml_dataset.csv")

print("=" * 70)
print("VALIDATING ML DATASET")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

# ============================================================
# 1. BASIC INFORMATION
# ============================================================

print("\nDataset shape:")
print(df.shape)

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDuplicate student-module records:")
print(
    df.duplicated(
        subset=[
            "id_student",
            "code_module",
            "code_presentation"
        ]
    ).sum()
)


# ============================================================
# 2. TARGET VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("TARGET VALIDATION")
print("=" * 70)

print("\nFuture average score:")
print(
    df["future_average_score"].describe()
)

print("\nScores outside 0-100:")

invalid_scores = df[
    (df["future_average_score"] < 0)
    | (df["future_average_score"] > 100)
]

print(len(invalid_scores))


# ============================================================
# 3. CHECK FIRST TWO ASSESSMENTS
# ============================================================

print("\n" + "=" * 70)
print("EARLY PERFORMANCE FEATURES")
print("=" * 70)

early_columns = [
    "first_score",
    "second_score",
    "early_avg_score",
    "early_min_score",
    "early_max_score",
    "score_trend"
]

print(
    df[early_columns].describe()
)


# ============================================================
# 4. CHECK ENGAGEMENT FEATURES
# ============================================================

print("\n" + "=" * 70)
print("TIME-AWARE ENGAGEMENT")
print("=" * 70)

engagement_columns = [
    "clicks_before_cutoff",
    "active_days_before_cutoff",
    "unique_resources_before_cutoff",
    "vle_records_before_cutoff",
    "average_daily_clicks_before_cutoff"
]

print(
    df[engagement_columns].describe()
)


# ============================================================
# 5. CHECK CATEGORICAL FEATURES
# ============================================================

print("\n" + "=" * 70)
print("CATEGORICAL FEATURES")
print("=" * 70)

categorical_columns = [
    "code_module",
    "code_presentation",
    "gender",
    "region",
    "highest_education",
    "imd_band",
    "age_band",
    "disability"
]

for column in categorical_columns:
    print(f"\n{column}:")
    print(df[column].value_counts(dropna=False).head(15))


# ============================================================
# 6. TARGET DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("TARGET DISTRIBUTION")
print("=" * 70)

print(
    df["future_performance_category"]
    .value_counts()
)

print("\nRisk distribution:")

print(
    df["future_risk_level"]
    .value_counts()
)


# ============================================================
# 7. MODULE DISTRIBUTION
# ============================================================

print("\n" + "=" * 70)
print("MODULE DISTRIBUTION")
print("=" * 70)

print(
    df["code_module"].value_counts()
)


# ============================================================
# 8. CORRELATION WITH TARGET
# ============================================================

print("\n" + "=" * 70)
print("NUMERIC FEATURE CORRELATION WITH TARGET")
print("=" * 70)

numeric_columns = [
    "first_score",
    "second_score",
    "early_avg_score",
    "early_min_score",
    "early_max_score",
    "score_trend",
    "clicks_before_cutoff",
    "active_days_before_cutoff",
    "unique_resources_before_cutoff",
    "vle_records_before_cutoff",
    "average_daily_clicks_before_cutoff",
    "num_of_prev_attempts",
    "studied_credits"
]

correlation = (
    df[numeric_columns + ["future_average_score"]]
    .corr()["future_average_score"]
    .sort_values(ascending=False)
)

print(correlation)


# ============================================================
# 9. LEAKAGE CHECK
# ============================================================

print("\n" + "=" * 70)
print("LEAKAGE CHECK")
print("=" * 70)

forbidden_columns = [
    "future_average_score",
    "future_min_score",
    "future_max_score",
    "future_assessment_count",
    "future_performance_category",
    "future_risk_level"
]

print("\nColumns that MUST NOT be used as input features:")

for column in forbidden_columns:
    print("-", column)


# ============================================================
# 10. FINAL CHECK
# ============================================================

print("\n" + "=" * 70)
print("ML DATASET VALIDATION COMPLETED")
print("=" * 70)