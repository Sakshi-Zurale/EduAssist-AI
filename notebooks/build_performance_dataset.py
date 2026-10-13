import pandas as pd
from pathlib import Path

# Dataset path
DATA_DIR = Path("../Dataset/OULAD")

# Output path
OUTPUT_DIR = Path("../data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


print("=" * 70)
print("LOADING DATA")
print("=" * 70)

# Load files
student_info = pd.read_csv(
    DATA_DIR / "studentInfo.csv"
)

student_assessment = pd.read_csv(
    DATA_DIR / "studentAssessment.csv"
)

assessments = pd.read_csv(
    DATA_DIR / "assessments.csv"
)

print("studentInfo:", student_info.shape)
print("studentAssessment:", student_assessment.shape)
print("assessments:", assessments.shape)


print("\n" + "=" * 70)
print("JOINING ASSESSMENT DATA")
print("=" * 70)

# Join student assessment with assessment metadata
assessment_data = student_assessment.merge(
    assessments,
    on="id_assessment",
    how="left"
)

print("After assessment join:", assessment_data.shape)


print("\n" + "=" * 70)
print("JOINING STUDENT INFORMATION")
print("=" * 70)

# Join with student information
performance_data = assessment_data.merge(
    student_info,
    on=[
        "id_student",
        "code_module",
        "code_presentation"
    ],
    how="left"
)

print("Final performance dataset:", performance_data.shape)


print("\n" + "=" * 70)
print("SELECTING IMPORTANT COLUMNS")
print("=" * 70)

columns = [
    "id_student",
    "code_module",
    "code_presentation",
    "id_assessment",
    "assessment_type",
    "date",
    "weight",
    "date_submitted",
    "is_banked",
    "score",
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

performance_data = performance_data[columns]

print("Selected columns:")
print(performance_data.columns.tolist())


print("\n" + "=" * 70)
print("HANDLING MISSING SCORES")
print("=" * 70)

missing_scores = performance_data["score"].isna().sum()

print("Missing scores before removal:", missing_scores)

# A missing score means there is no usable assessment score.
# We will remove these rows from the performance dataset.
performance_data = performance_data.dropna(
    subset=["score"]
)

print(
    "Missing scores after removal:",
    performance_data["score"].isna().sum()
)


print("\n" + "=" * 70)
print("FINAL DATASET INFORMATION")
print("=" * 70)

print("Rows:", len(performance_data))
print("Columns:", len(performance_data.columns))

print("\nFirst 5 rows:")
print(
    performance_data.head().to_string(index=False)
)


print("\n" + "=" * 70)
print("FINAL RESULT DISTRIBUTION")
print("=" * 70)

print(
    performance_data["final_result"].value_counts()
)


print("\n" + "=" * 70)
print("SAVING DATASET")
print("=" * 70)

output_file = OUTPUT_DIR / "student_performance.csv"

performance_data.to_csv(
    output_file,
    index=False
)

print("Saved successfully:")
print(output_file)

print("\n" + "=" * 70)
print("STEP 4 COMPLETED")
print("=" * 70)