import pandas as pd
from pathlib import Path

DATA_FILE = Path("../data/processed/eduassist_student_dataset.csv")

df = pd.read_csv(DATA_FILE)

print("=" * 70)
print("EDUASSIST AI DATASET VALIDATION")
print("=" * 70)


# ---------------------------------------------------------
# 1. DATASET SIZE
# ---------------------------------------------------------

print("\nDataset shape:")
print(df.shape)


# ---------------------------------------------------------
# 2. DUPLICATES
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("1. DUPLICATES")
print("=" * 70)

print("Duplicate rows:", df.duplicated().sum())

print(
    "Duplicate student IDs:",
    df["id_student"].duplicated().sum()
)


# ---------------------------------------------------------
# 3. MISSING VALUES
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("2. MISSING VALUES")
print("=" * 70)

missing = df.isnull().sum()

print(
    missing[missing > 0]
    .sort_values(ascending=False)
)


# ---------------------------------------------------------
# 4. PERFORMANCE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("3. PERFORMANCE")
print("=" * 70)

print(
    df["average_score"].describe()
)

print("\nPerformance categories:")
print(
    df["performance_category"]
    .value_counts()
)


# ---------------------------------------------------------
# 5. ENGAGEMENT
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("4. ENGAGEMENT")
print("=" * 70)

print(
    df[
        [
            "total_clicks",
            "active_days",
            "unique_vle_resources",
            "average_daily_clicks",
            "engagement_score"
        ]
    ].describe()
)


# ---------------------------------------------------------
# 6. RISK
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("5. RISK LEVEL")
print("=" * 70)

print(
    df["risk_level"]
    .value_counts()
)


# ---------------------------------------------------------
# 7. RISK VS PERFORMANCE
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("6. RISK VS PERFORMANCE")
print("=" * 70)

risk_table = pd.crosstab(
    df["risk_level"],
    df["performance_category"]
)

print(risk_table)


# ---------------------------------------------------------
# 8. RISK VS FINAL RESULT
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("7. RISK VS FINAL RESULT")
print("=" * 70)

result_table = pd.crosstab(
    df["risk_level"],
    df["final_result"]
)

print(result_table)


# ---------------------------------------------------------
# 9. PERFORMANCE VS FINAL RESULT
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("8. PERFORMANCE VS FINAL RESULT")
print("=" * 70)

performance_result = pd.crosstab(
    df["performance_category"],
    df["final_result"]
)

print(performance_result)


# ---------------------------------------------------------
# 10. MODULE ANALYSIS
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("9. MODULE ANALYSIS")
print("=" * 70)

module_summary = (
    df.groupby("code_module")
    .agg(
        students=("id_student", "count"),
        average_score=("average_score", "mean"),
        average_engagement=("engagement_score", "mean"),
        average_clicks=("total_clicks", "mean")
    )
    .round(2)
)

print(module_summary)


# ---------------------------------------------------------
# 11. SCORE + ENGAGEMENT CORRELATION
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("10. PERFORMANCE-ENGAGEMENT RELATIONSHIP")
print("=" * 70)

correlation = df[
    [
        "average_score",
        "total_clicks",
        "active_days",
        "unique_vle_resources",
        "average_daily_clicks",
        "engagement_score"
    ]
].corr()

print(
    correlation["average_score"]
    .sort_values(ascending=False)
)


print("\n" + "=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)