import pandas as pd
from pathlib import Path

DATA_DIR = Path("../Dataset/OULAD")

assessments = pd.read_csv(
    DATA_DIR / "assessments.csv"
)

student_assessment = pd.read_csv(
    DATA_DIR / "studentAssessment.csv"
)

print("=" * 70)
print("ASSESSMENT TIMELINE ANALYSIS")
print("=" * 70)


# ---------------------------------------------------------
# 1. JOIN ASSESSMENT INFORMATION
# ---------------------------------------------------------

data = student_assessment.merge(
    assessments,
    on="id_assessment",
    how="left"
)

print("\nDataset shape:")
print(data.shape)


# ---------------------------------------------------------
# 2. ASSESSMENT TYPES
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("ASSESSMENT TYPES")
print("=" * 70)

print(
    data["assessment_type"]
    .value_counts()
)


# ---------------------------------------------------------
# 3. ASSESSMENT DATES
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("ASSESSMENT DATES")
print("=" * 70)

print(
    data["date"].describe()
)


# ---------------------------------------------------------
# 4. UNIQUE ASSESSMENTS PER MODULE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("ASSESSMENTS PER MODULE")
print("=" * 70)

assessment_counts = (
    assessments
    .groupby(
        ["code_module", "code_presentation"]
    )
    .agg(
        assessment_count=("id_assessment", "count"),
        earliest_date=("date", "min"),
        latest_date=("date", "max")
    )
    .reset_index()
)

print(
    assessment_counts.to_string(index=False)
)


# ---------------------------------------------------------
# 5. ASSESSMENT TYPES PER MODULE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("ASSESSMENT TYPES PER MODULE")
print("=" * 70)

type_table = pd.crosstab(
    assessments["code_module"],
    assessments["assessment_type"]
)

print(type_table)


# ---------------------------------------------------------
# 6. EXAMPLE STUDENT TIMELINE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("EXAMPLE STUDENT TIMELINE")
print("=" * 70)

student_id = data["id_student"].iloc[0]

student_history = (
    data[
        data["id_student"] == student_id
    ]
    .sort_values("date")
)

print(
    student_history[
        [
            "id_student",
            "code_module",
            "code_presentation",
            "id_assessment",
            "assessment_type",
            "date",
            "date_submitted",
            "score"
        ]
    ].to_string(index=False)
)


print("\n" + "=" * 70)
print("TIMELINE ANALYSIS COMPLETED")
print("=" * 70)