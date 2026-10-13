from pathlib import Path
import pandas as pd


# ---------------------------------------------------------
# PATH
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PERFORMANCE_DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "student_performance.csv"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

performance_data = pd.read_csv(
    PERFORMANCE_DATA_PATH
)


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def clean_value(value):
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


# ---------------------------------------------------------
# ASSESSMENT PERFORMANCE
# ---------------------------------------------------------

def analyze_assessment_performance(student_id):

    rows = performance_data[
        performance_data["id_student"] == student_id
    ].copy()

    if rows.empty:
        return None

    rows = rows.dropna(
        subset=["score"]
    )

    if rows.empty:
        return None

    # Sort by assessment date where available
    if "date" in rows.columns:
        rows = rows.sort_values("date")

    # -----------------------------------------------------
    # Basic statistics
    # -----------------------------------------------------

    average_score = rows["score"].mean()
    highest_score = rows["score"].max()
    lowest_score = rows["score"].min()

    # -----------------------------------------------------
    # Consistency
    # -----------------------------------------------------

    score_std = rows["score"].std()

    if pd.isna(score_std):
        score_std = 0

    if score_std <= 5:
        consistency = "Highly Consistent"
    elif score_std <= 10:
        consistency = "Consistent"
    elif score_std <= 15:
        consistency = "Moderately Variable"
    else:
        consistency = "Highly Variable"

    # -----------------------------------------------------
    # First vs latest
    # -----------------------------------------------------

    first_score = float(
        rows.iloc[0]["score"]
    )

    latest_score = float(
        rows.iloc[-1]["score"]
    )

    change = latest_score - first_score

    if change > 5:
        trend = "Improving"
    elif change < -5:
        trend = "Declining"
    else:
        trend = "Stable"

    # -----------------------------------------------------
    # Weak assessments
    # -----------------------------------------------------

    weak_assessments = rows[
        rows["score"] < 65
    ]

    # -----------------------------------------------------
    # Strong assessments
    # -----------------------------------------------------

    strong_assessments = rows[
        rows["score"] >= 80
    ]

    # -----------------------------------------------------
    # Assessment type analysis
    # -----------------------------------------------------

    assessment_type_analysis = []

    if "assessment_type" in rows.columns:

        for assessment_type, group in rows.groupby(
            "assessment_type"
        ):

            assessment_type_analysis.append(
                {
                    "assessment_type": clean_value(
                        assessment_type
                    ),
                    "count": int(len(group)),
                    "average_score": round(
                        float(group["score"].mean()),
                        2
                    ),
                    "highest_score": round(
                        float(group["score"].max()),
                        2
                    ),
                    "lowest_score": round(
                        float(group["score"].min()),
                        2
                    )
                }
            )

    # -----------------------------------------------------
    # Academic priority
    # -----------------------------------------------------

    reasons = []

    if average_score < 50:
        reasons.append(
            "Overall assessment performance is low"
        )

    elif average_score < 65:
        reasons.append(
            "Overall assessment performance needs improvement"
        )

    if trend == "Declining":
        reasons.append(
            "Recent assessment performance is declining"
        )

    if len(weak_assessments) > 0:
        reasons.append(
            f"{len(weak_assessments)} assessment(s) "
            "scored below 65"
        )

    if consistency == "Highly Variable":
        reasons.append(
            "Assessment performance is inconsistent"
        )

    # -----------------------------------------------------
    # Priority level
    # -----------------------------------------------------

    if (
        average_score < 50
        or trend == "Declining"
        or len(weak_assessments) >= 2
    ):
        priority = "High"

    elif (
        average_score < 65
        or len(weak_assessments) == 1
        or consistency == "Highly Variable"
    ):
        priority = "Medium"

    else:
        priority = "Low"

    # -----------------------------------------------------
    # Return analysis
    # -----------------------------------------------------

    return {
        "assessment_count": int(len(rows)),

        "average_score": round(
            float(average_score),
            2
        ),

        "highest_score": round(
            float(highest_score),
            2
        ),

        "lowest_score": round(
            float(lowest_score),
            2
        ),

        "score_standard_deviation": round(
            float(score_std),
            2
        ),

        "consistency": consistency,

        "first_score": round(
            first_score,
            2
        ),

        "latest_score": round(
            latest_score,
            2
        ),

        "score_change": round(
            float(change),
            2
        ),

        "trend": trend,

        "weak_assessment_count": int(
            len(weak_assessments)
        ),

        "strong_assessment_count": int(
            len(strong_assessments)
        ),

        "assessment_type_analysis":
            assessment_type_analysis,

        "academic_priority": {
            "priority": priority,
            "reasons": reasons
        }
    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    student_id = 11391

    result = analyze_assessment_performance(
        student_id
    )

    print("\n====================================")
    print(" EDUASSIST WEAKNESS ANALYSIS")
    print("====================================")

    if result is None:

        print(
            f"\nStudent {student_id} not found."
        )

    else:

        print(
            f"\nStudent ID: {student_id}"
        )

        print(
            "\nAssessment Analysis:"
        )

        print(result)