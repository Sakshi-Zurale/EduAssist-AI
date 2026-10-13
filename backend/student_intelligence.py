from pathlib import Path
import pandas as pd

from .weakness_analysis import analyze_assessment_performance

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

STUDENT_DATA_PATH = PROCESSED_DIR / "eduassist_student_dataset.csv"
ML_DATA_PATH = PROCESSED_DIR / "eduassist_ml_dataset.csv"
PERFORMANCE_DATA_PATH = PROCESSED_DIR / "student_performance.csv"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

student_data = pd.read_csv(STUDENT_DATA_PATH)
ml_data = pd.read_csv(ML_DATA_PATH)
performance_data = pd.read_csv(PERFORMANCE_DATA_PATH)


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def clean_value(value):
    """
    Convert pandas/numpy values into JSON-friendly Python values.
    """
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


# ---------------------------------------------------------
# PERFORMANCE ANALYSIS
# ---------------------------------------------------------

def get_performance_analysis(student_id):

    student_rows = student_data[
        student_data["id_student"] == student_id
    ]

    if student_rows.empty:
        return None

    row = student_rows.iloc[0]

    return {
        "average_score": clean_value(
            row["average_score"]
        ),
        "highest_score": clean_value(
            row["highest_score"]
        ),
        "lowest_score": clean_value(
            row["lowest_score"]
        ),
        "assessment_count": clean_value(
            row["assessment_count"]
        ),
        "performance_category": clean_value(
            row["performance_category"]
        ),
        "exam_average_score": clean_value(
            row["exam_average_score"]
        ),
        "tma_average_score": clean_value(
            row["tma_average_score"]
        ),
        "cma_average_score": clean_value(
            row["cma_average_score"]
        ),
    }


# ---------------------------------------------------------
# ENGAGEMENT ANALYSIS
# ---------------------------------------------------------

def get_engagement_analysis(student_id):

    student_rows = student_data[
        student_data["id_student"] == student_id
    ]

    if student_rows.empty:
        return None

    row = student_rows.iloc[0]

    return {
        "total_clicks": clean_value(
            row["total_clicks"]
        ),
        "active_days": clean_value(
            row["active_days"]
        ),
        "unique_vle_resources": clean_value(
            row["unique_vle_resources"]
        ),
        "vle_records": clean_value(
            row["vle_records"]
        ),
        "average_daily_clicks": clean_value(
            row["average_daily_clicks"]
        ),
        "engagement_score": clean_value(
            row["engagement_score"]
        ),
    }


# ---------------------------------------------------------
# ASSESSMENT ANALYSIS
# ---------------------------------------------------------

def get_assessment_analysis(student_id):

    rows = performance_data[
        performance_data["id_student"] == student_id
    ].copy()

    if rows.empty:
        return {
            "total_assessments": 0,
            "assessment_types": []
        }

    assessment_types = []

    for assessment_type, group in rows.groupby(
        "assessment_type"
    ):

        assessment_types.append(
            {
                "assessment_type": assessment_type,
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

    return {
        "total_assessments": int(len(rows)),
        "assessment_types": assessment_types
    }


# ---------------------------------------------------------
# TREND ANALYSIS
# ---------------------------------------------------------

def get_trend_analysis(student_id):

    rows = performance_data[
        performance_data["id_student"] == student_id
    ].copy()

    if rows.empty:
        return {
            "trend": "Unknown",
            "change": None
        }

    rows = rows.dropna(
        subset=["date", "score"]
    ).sort_values("date")

    if len(rows) < 2:
        return {
            "trend": "Insufficient data",
            "change": None
        }

    first_score = float(
        rows.iloc[0]["score"]
    )

    last_score = float(
        rows.iloc[-1]["score"]
    )

    change = last_score - first_score

    if change > 5:
        trend = "Improving"

    elif change < -5:
        trend = "Declining"

    else:
        trend = "Stable"

    return {
        "first_score": round(
            first_score,
            2
        ),
        "latest_score": round(
            last_score,
            2
        ),
        "change": round(
            change,
            2
        ),
        "trend": trend
    }


# ---------------------------------------------------------
# PROFILE
# ---------------------------------------------------------

def get_student_profile(student_id):

    rows = student_data[
        student_data["id_student"] == student_id
    ]

    if rows.empty:
        return None

    row = rows.iloc[0]

    profile_fields = [
        "gender",
        "region",
        "highest_education",
        "imd_band",
        "age_band",
        "num_of_prev_attempts",
        "studied_credits",
        "disability"
    ]

    profile = {}

    for field in profile_fields:

        if field in row:

            profile[field] = clean_value(
                row[field]
            )

    return profile


# ---------------------------------------------------------
# ML INTELLIGENCE
# ---------------------------------------------------------

def get_ml_context(student_id):

    rows = ml_data[
        ml_data["id_student"] == student_id
    ]

    if rows.empty:
        return {
            "available": False
        }

    # Current prototype uses the first eligible
    # student-module-presentation record.
    row = rows.iloc[0]

    return {
        "available": True,

        "module": clean_value(
            row["code_module"]
        ),

        "presentation": clean_value(
            row["code_presentation"]
        ),

        "early_average_score": clean_value(
            row["early_avg_score"]
        ),

        "score_trend": clean_value(
            row["score_trend"]
        ),

        "early_assessment_count": clean_value(
            row["early_assessment_count"]
        ),

        "early_engagement": {
            "clicks_before_cutoff": clean_value(
                row["clicks_before_cutoff"]
            ),

            "active_days_before_cutoff": clean_value(
                row["active_days_before_cutoff"]
            ),

            "unique_resources_before_cutoff": clean_value(
                row["unique_resources_before_cutoff"]
            )
        }
    }


# ---------------------------------------------------------
# ACADEMIC PRIORITY
# ---------------------------------------------------------

def determine_academic_priority(
    performance,
    engagement,
    trend
):

    reasons = []

    average_score = performance["average_score"]

    engagement_score = engagement[
        "engagement_score"
    ]

    if average_score < 50:

        reasons.append(
            "Very low academic performance"
        )

    elif average_score < 65:

        reasons.append(
            "Academic performance needs improvement"
        )

    if engagement_score < 5:

        reasons.append(
            "Very low learning engagement"
        )

    elif engagement_score < 10:

        reasons.append(
            "Low learning engagement"
        )

    if trend["trend"] == "Declining":

        reasons.append(
            "Recent performance is declining"
        )

    if (
        average_score >= 80
        and engagement_score >= 10
    ):

        priority = "Low"

    elif (
        average_score < 50
        or engagement_score < 5
    ):

        priority = "High"

    else:

        priority = "Medium"

    return {
        "priority": priority,
        "reasons": reasons
    }


# ---------------------------------------------------------
# COMPLETE STUDENT INTELLIGENCE
# ---------------------------------------------------------

def get_student_intelligence(student_id):

    performance = get_performance_analysis(
        student_id
    )

    if performance is None:
        return None

    engagement = get_engagement_analysis(
        student_id
    )

    assessment = get_assessment_analysis(
        student_id
    )

    trend = get_trend_analysis(
        student_id
    )

    profile = get_student_profile(
        student_id
    )

    ml_context = get_ml_context(
        student_id
    )

    weakness_analysis = analyze_assessment_performance(
        student_id
    )

    priority = determine_academic_priority(
        performance,
        engagement,
        trend
    )

    return {
        "student_id": int(student_id),

        "profile": profile,

        "performance": performance,

        "assessment_analysis": assessment,

        "engagement": engagement,

        "trend": trend,

        "weakness_analysis": weakness_analysis,

        "academic_priority": priority,

        "ml_context": ml_context
    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    student_id = 11391

    intelligence = get_student_intelligence(
        student_id
    )

    if intelligence is None:

        print(
            f"Student {student_id} not found."
        )

    else:

        print(
            "\n===================================="
        )

        print(
            " EDUASSIST STUDENT INTELLIGENCE"
        )

        print(
            "===================================="
        )

        print(
            f"\nStudent ID: "
            f"{intelligence['student_id']}"
        )

        print(
            "\nProfile:"
        )

        print(
            intelligence["profile"]
        )

        print(
            "\nPerformance:"
        )

        print(
            intelligence["performance"]
        )

        print(
            "\nAssessment Analysis:"
        )

        print(
            intelligence["assessment_analysis"]
        )

        print(
            "\nEngagement:"
        )

        print(
            intelligence["engagement"]
        )

        print(
            "\nTrend:"
        )

        print(
            intelligence["trend"]
        )

        print(
            "\nWeakness Analysis:"
        )

        print(
            intelligence["weakness_analysis"]
        )

        print(
            "\nAcademic Priority:"
        )

        print(
            intelligence["academic_priority"]
        )

        print(
            "\nML Context:"
        )

        print(
            intelligence["ml_context"]
        )