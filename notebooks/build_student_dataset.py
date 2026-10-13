import pandas as pd
from pathlib import Path

DATA_DIR = Path("../data/processed")
OUTPUT_DIR = Path("../data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


print("=" * 70)
print("BUILDING EDUASSIST AI STUDENT DATASET")
print("=" * 70)


# ---------------------------------------------------------
# 1. LOAD DATASETS
# ---------------------------------------------------------

print("\nLoading performance dataset...")

performance = pd.read_csv(
    DATA_DIR / "student_performance.csv"
)

print("Performance:", performance.shape)


print("\nLoading engagement dataset...")

engagement = pd.read_csv(
    DATA_DIR / "student_engagement.csv"
)

print("Engagement:", engagement.shape)


# ---------------------------------------------------------
# 2. CREATE STUDENT-LEVEL PERFORMANCE FEATURES
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("CREATING STUDENT PERFORMANCE FEATURES")
print("=" * 70)


student_performance = (
    performance
    .groupby("id_student")
    .agg(
        average_score=("score", "mean"),
        highest_score=("score", "max"),
        lowest_score=("score", "min"),
        assessment_count=("score", "count"),
        average_weight=("weight", "mean"),
        exam_average_score=(
            "score",
            lambda x: x[
                performance.loc[x.index, "assessment_type"]
                == "Exam"
            ].mean()
        ),
        tma_average_score=(
            "score",
            lambda x: x[
                performance.loc[x.index, "assessment_type"]
                == "TMA"
            ].mean()
        ),
        cma_average_score=(
            "score",
            lambda x: x[
                performance.loc[x.index, "assessment_type"]
                == "CMA"
            ].mean()
        )
    )
    .reset_index()
)


# ---------------------------------------------------------
# 3. ADD STUDENT PROFILE INFORMATION
# ---------------------------------------------------------

print("\nAdding student profile information...")


student_profile = (
    performance
    .sort_values("date_submitted")
    .groupby("id_student")
    .first()
    .reset_index()
)


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
    "disability",
    "final_result"
]

student_profile = student_profile[
    profile_columns
]


# ---------------------------------------------------------
# 4. MERGE PERFORMANCE + PROFILE
# ---------------------------------------------------------

student_data = student_performance.merge(
    student_profile,
    on="id_student",
    how="left"
)


# ---------------------------------------------------------
# 5. MERGE ENGAGEMENT
# ---------------------------------------------------------

print("\nMerging engagement data...")


student_data = student_data.merge(
    engagement,
    on="id_student",
    how="left"
)


# ---------------------------------------------------------
# 6. HANDLE STUDENTS WITHOUT VLE DATA
# ---------------------------------------------------------

engagement_columns = [
    "total_clicks",
    "active_days",
    "unique_vle_resources",
    "vle_records",
    "average_daily_clicks",
    "engagement_score"
]

student_data[engagement_columns] = (
    student_data[engagement_columns]
    .fillna(0)
)


# ---------------------------------------------------------
# 7. CREATE BASIC PERFORMANCE CATEGORY
# ---------------------------------------------------------

print("\nCreating performance category...")


def performance_category(score):

    if score < 50:
        return "Low"

    elif score < 65:
        return "Needs Improvement"

    elif score < 80:
        return "Good"

    else:
        return "Excellent"


student_data["performance_category"] = (
    student_data["average_score"]
    .apply(performance_category)
)


# ---------------------------------------------------------
# 8. CREATE BASIC RISK CATEGORY
# ---------------------------------------------------------

print("Creating baseline risk category...")


def risk_category(row):

    score = row["average_score"]
    engagement_score = row["engagement_score"]

    if score < 50 or engagement_score < 5:
        return "High"

    elif score < 65 or engagement_score < 10:
        return "Medium"

    else:
        return "Low"


student_data["risk_level"] = (
    student_data.apply(
        risk_category,
        axis=1
    )
)


# ---------------------------------------------------------
# 9. SAVE DATASET
# ---------------------------------------------------------

output_file = (
    OUTPUT_DIR /
    "eduassist_student_dataset.csv"
)


student_data.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# 10. DISPLAY RESULTS
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL EDUASSIST STUDENT DATASET")
print("=" * 70)

print("Rows:", len(student_data))
print("Columns:", len(student_data.columns))

print("\nColumns:")
print(student_data.columns.tolist())

print("\nFirst 5 rows:")
print(
    student_data.head().to_string(index=False)
)


print("\nPerformance categories:")
print(
    student_data["performance_category"]
    .value_counts()
)


print("\nRisk levels:")
print(
    student_data["risk_level"]
    .value_counts()
)


print("\nMissing values:")
print(
    student_data.isnull().sum()[
        student_data.isnull().sum() > 0
    ]
)


print("\nSaved successfully:")
print(output_file)


print("\n" + "=" * 70)
print("STEP 7 COMPLETED")
print("=" * 70)