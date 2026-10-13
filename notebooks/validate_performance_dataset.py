import pandas as pd
from pathlib import Path

DATA_FILE = Path("../data/processed/student_performance.csv")

df = pd.read_csv(DATA_FILE)

print("=" * 70)
print("PERFORMANCE DATASET VALIDATION")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


print("\n" + "=" * 70)
print("1. DUPLICATE RECORDS")
print("=" * 70)

print("Duplicate rows:", df.duplicated().sum())


print("\n" + "=" * 70)
print("2. MISSING VALUES")
print("=" * 70)

missing = df.isnull().sum()

print(missing[missing > 0])


print("\n" + "=" * 70)
print("3. SCORE STATISTICS")
print("=" * 70)

print(df["score"].describe())


print("\n" + "=" * 70)
print("4. SCORE RANGE CHECK")
print("=" * 70)

print("Minimum score:", df["score"].min())
print("Maximum score:", df["score"].max())

print(
    "Scores outside 0-100:",
    ((df["score"] < 0) | (df["score"] > 100)).sum()
)


print("\n" + "=" * 70)
print("5. ASSESSMENT TYPES")
print("=" * 70)

print(df["assessment_type"].value_counts())


print("\n" + "=" * 70)
print("6. STUDENT COUNTS")
print("=" * 70)

print("Unique students:", df["id_student"].nunique())

print(
    "Average assessments per student:",
    round(
        len(df) / df["id_student"].nunique(),
        2
    )
)


print("\n" + "=" * 70)
print("7. MODULE DISTRIBUTION")
print("=" * 70)

print(df["code_module"].value_counts())


print("\n" + "=" * 70)
print("8. FINAL RESULT")
print("=" * 70)

print(df["final_result"].value_counts())


print("\n" + "=" * 70)
print("9. AVERAGE SCORE BY FINAL RESULT")
print("=" * 70)

print(
    df.groupby("final_result")["score"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)


print("\n" + "=" * 70)
print("10. AVERAGE SCORE BY ASSESSMENT TYPE")
print("=" * 70)

print(
    df.groupby("assessment_type")["score"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)


print("\n" + "=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)