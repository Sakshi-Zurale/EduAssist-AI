import pandas as pd
from pathlib import Path

DATA_DIR = Path("../Dataset/OULAD")
OUTPUT_DIR = Path("../data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


print("=" * 70)
print("BUILDING STUDENT ENGAGEMENT DATASET")
print("=" * 70)


# ---------------------------------------------------------
# 1. LOAD STUDENT VLE DATA
# ---------------------------------------------------------

print("\nLoading studentVle.csv...")

student_vle = pd.read_csv(
    DATA_DIR / "studentVle.csv"
)

print("Rows:", len(student_vle))
print("Columns:", len(student_vle.columns))


# ---------------------------------------------------------
# 2. BASIC INFORMATION
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("BASIC ENGAGEMENT INFORMATION")
print("=" * 70)

print("Unique students:",
      student_vle["id_student"].nunique())

print("Unique VLE resources:",
      student_vle["id_site"].nunique())

print("Total clicks:",
      student_vle["sum_click"].sum())


# ---------------------------------------------------------
# 3. AGGREGATE STUDENT ENGAGEMENT
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("CALCULATING STUDENT ENGAGEMENT FEATURES")
print("=" * 70)


engagement = (
    student_vle
    .groupby("id_student")
    .agg(
        total_clicks=("sum_click", "sum"),
        active_days=("date", "nunique"),
        unique_vle_resources=("id_site", "nunique"),
        vle_records=("id_site", "count")
    )
    .reset_index()
)


# ---------------------------------------------------------
# 4. CALCULATE AVERAGE DAILY CLICKS
# ---------------------------------------------------------

engagement["average_daily_clicks"] = (
    engagement["total_clicks"]
    / engagement["active_days"]
)


# ---------------------------------------------------------
# 5. CALCULATE A SIMPLE ENGAGEMENT SCORE
# ---------------------------------------------------------

print("\nCreating normalized engagement score...")


def min_max_normalize(series):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return 0

    return (
        (series - minimum)
        / (maximum - minimum)
    )


click_score = min_max_normalize(
    engagement["total_clicks"]
)

active_day_score = min_max_normalize(
    engagement["active_days"]
)

resource_score = min_max_normalize(
    engagement["unique_vle_resources"]
)


engagement["engagement_score"] = (
    0.5 * click_score
    + 0.3 * active_day_score
    + 0.2 * resource_score
) * 100


# ---------------------------------------------------------
# 6. SAVE DATASET
# ---------------------------------------------------------

output_file = (
    OUTPUT_DIR /
    "student_engagement.csv"
)


engagement.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# 7. DISPLAY RESULTS
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("ENGAGEMENT DATASET")
print("=" * 70)

print("Rows:", len(engagement))
print("Columns:", len(engagement.columns))

print("\nColumns:")
print(engagement.columns.tolist())

print("\nFirst 5 rows:")
print(
    engagement.head().to_string(index=False)
)

print("\nEngagement score statistics:")
print(
    engagement["engagement_score"].describe()
)

print("\nSaved successfully:")
print(output_file)

print("\n" + "=" * 70)
print("STEP 6 COMPLETED")
print("=" * 70)