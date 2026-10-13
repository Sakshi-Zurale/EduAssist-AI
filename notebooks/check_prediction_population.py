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
print("CHECKING ML PREDICTION POPULATION")
print("=" * 70)


# ---------------------------------------------------------
# 1. JOIN ASSESSMENT DATE
# ---------------------------------------------------------

data = student_assessment.merge(
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


# Remove records without an assessment date
data = data.dropna(
    subset=["date"]
)


# Remove records without a score
data = data.dropna(
    subset=["score"]
)


# ---------------------------------------------------------
# 2. SORT STUDENT ASSESSMENTS
# ---------------------------------------------------------

data = data.sort_values(
    [
        "id_student",
        "code_module",
        "code_presentation",
        "date"
    ]
)


# ---------------------------------------------------------
# 3. NUMBER ASSESSMENTS FOR EACH STUDENT
# ---------------------------------------------------------

data["assessment_number"] = (
    data
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .cumcount() + 1
)


print("\nTotal valid assessment records:")
print(len(data))


# ---------------------------------------------------------
# 4. STUDENT-MODULE PRESENTATIONS
# ---------------------------------------------------------

student_modules = (
    data
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .size()
    .reset_index(
        name="assessment_count"
    )
)


print("\n" + "=" * 70)
print("ASSESSMENTS PER STUDENT-MODULE")
print("=" * 70)

print(
    student_modules["assessment_count"]
    .describe()
)


# ---------------------------------------------------------
# 5. STUDENTS WITH AT LEAST 3 ASSESSMENTS
# ---------------------------------------------------------

eligible = student_modules[
    student_modules["assessment_count"] >= 3
]

print("\n" + "=" * 70)
print("ELIGIBLE STUDENT-MODULE RECORDS")
print("=" * 70)

print(
    "At least 3 assessments:",
    len(eligible)
)


# ---------------------------------------------------------
# 6. STUDENTS WITH AT LEAST 4 ASSESSMENTS
# ---------------------------------------------------------

eligible_4 = student_modules[
    student_modules["assessment_count"] >= 4
]

print(
    "At least 4 assessments:",
    len(eligible_4)
)


# ---------------------------------------------------------
# 7. STUDENTS WITH AT LEAST 5 ASSESSMENTS
# ---------------------------------------------------------

eligible_5 = student_modules[
    student_modules["assessment_count"] >= 5
]

print(
    "At least 5 assessments:",
    len(eligible_5)
)


# ---------------------------------------------------------
# 8. FIRST TWO → FUTURE ASSESSMENTS
# ---------------------------------------------------------

eligible_future = student_modules[
    student_modules["assessment_count"] > 2
]

print("\n" + "=" * 70)
print("FIRST 2 ASSESSMENTS → FUTURE PERFORMANCE")
print("=" * 70)

print(
    "Records with at least 3 assessments:",
    len(eligible_future)
)


# ---------------------------------------------------------
# 9. MODULE-WISE ELIGIBILITY
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("MODULE-WISE ELIGIBILITY")
print("=" * 70)

module_eligibility = (
    eligible_future
    .groupby("code_module")
    .size()
)

print(
    module_eligibility
)


# ---------------------------------------------------------
# 10. ASSESSMENT EXAMPLE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("EXAMPLE ELIGIBLE STUDENT")
print("=" * 70)

example = (
    data[
        data["assessment_number"] <= 5
    ]
    .groupby(
        [
            "id_student",
            "code_module",
            "code_presentation"
        ]
    )
    .filter(
        lambda x: len(x) >= 3
    )
)

if len(example) > 0:

    first_student = (
        example[
            [
                "id_student",
                "code_module",
                "code_presentation"
            ]
        ]
        .iloc[0]
    )

    student_id = first_student["id_student"]
    module = first_student["code_module"]
    presentation = first_student["code_presentation"]

    print(
        data[
            (data["id_student"] == student_id)
            &
            (data["code_module"] == module)
            &
            (data["code_presentation"] == presentation)
        ][
            [
                "assessment_number",
                "assessment_type",
                "date",
                "score"
            ]
        ].to_string(index=False)
    )


print("\n" + "=" * 70)
print("POPULATION CHECK COMPLETED")
print("=" * 70)