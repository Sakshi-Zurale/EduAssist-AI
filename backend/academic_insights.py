from typing import Dict, List, Optional


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def safe_float(value, default=0.0):
    """
    Safely convert a value to float.
    """
    if value is None:
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------
# PERFORMANCE INSIGHT
# ---------------------------------------------------------

def generate_performance_insight(performance: Dict) -> str:

    average_score = safe_float(
        performance.get("average_score")
    )

    category = performance.get(
        "performance_category",
        "Unknown"
    )

    if average_score >= 80:

        return (
            f"Academic performance is excellent with "
            f"an average score of {average_score:.1f}%."
        )

    elif average_score >= 65:

        return (
            f"Academic performance is good with "
            f"an average score of {average_score:.1f}%."
        )

    elif average_score >= 50:

        return (
            f"Academic performance needs improvement, "
            f"with an average score of {average_score:.1f}%."
        )

    return (
        f"Academic performance is currently low, "
        f"with an average score of {average_score:.1f}%."
    )


# ---------------------------------------------------------
# CONSISTENCY INSIGHT
# ---------------------------------------------------------

def generate_consistency_insight(
    weakness_analysis: Dict
) -> str:

    consistency = weakness_analysis.get(
        "consistency",
        "Unknown"
    )

    standard_deviation = safe_float(
        weakness_analysis.get(
            "score_standard_deviation"
        )
    )

    if consistency == "Highly Consistent":

        return (
            f"Assessment performance is highly consistent "
            f"with a score variation of {standard_deviation:.2f}."
        )

    elif consistency == "Consistent":

        return (
            f"Assessment performance is consistent "
            f"with a score variation of {standard_deviation:.2f}."
        )

    elif consistency == "Moderately Variable":

        return (
            f"Assessment performance shows moderate variation "
            f"with a score variation of {standard_deviation:.2f}."
        )

    elif consistency == "Highly Variable":

        return (
            f"Assessment performance is highly variable "
            f"with a score variation of {standard_deviation:.2f}."
        )

    return "Assessment consistency could not be determined."


# ---------------------------------------------------------
# TREND INSIGHT
# ---------------------------------------------------------

def generate_trend_insight(trend: Dict) -> str:

    trend_type = trend.get(
        "trend",
        "Unknown"
    )

    change = trend.get(
        "change"
    )

    if change is None:

        return (
            "There is not enough assessment history "
            "to determine a performance trend."
        )

    change = safe_float(change)

    if trend_type == "Improving":

        return (
            f"Performance is improving, with a "
            f"{change:.1f}-point increase from the first "
            f"to the latest assessment."
        )

    elif trend_type == "Declining":

        return (
            f"Performance is declining, with a "
            f"{abs(change):.1f}-point decrease from the first "
            f"to the latest assessment."
        )

    return (
        f"Performance is relatively stable, with a "
        f"{abs(change):.1f}-point change between the first "
        f"and latest assessment."
    )


# ---------------------------------------------------------
# WEAKNESS INSIGHT
# ---------------------------------------------------------

def generate_weakness_insight(
    weakness_analysis: Dict
) -> str:

    weak_count = int(
        weakness_analysis.get(
            "weak_assessment_count",
            0
        )
    )

    strong_count = int(
        weakness_analysis.get(
            "strong_assessment_count",
            0
        )
    )

    assessment_count = int(
        weakness_analysis.get(
            "assessment_count",
            0
        )
    )

    if assessment_count == 0:

        return (
            "There is not enough assessment data "
            "to identify academic strengths or weaknesses."
        )

    if weak_count == 0 and strong_count > 0:

        return (
            f"No weak assessments were identified. "
            f"{strong_count} assessment(s) scored 80% or above."
        )

    if weak_count == 1:

        return (
            "One assessment requires additional attention "
            "and should be reviewed for possible improvement."
        )

    if weak_count >= 2:

        return (
            f"{weak_count} assessments scored below 65%, "
            f"indicating areas that require focused improvement."
        )

    return (
        "Assessment results should be monitored for "
        "potential areas of weakness."
    )


# ---------------------------------------------------------
# ENGAGEMENT INSIGHT
# ---------------------------------------------------------

def generate_engagement_insight(
    engagement: Dict
) -> str:

    engagement_score = safe_float(
        engagement.get("engagement_score")
    )

    active_days = safe_float(
        engagement.get("active_days")
    )

    resources = safe_float(
        engagement.get("unique_vle_resources")
    )

    if engagement_score >= 20:

        level = "high"

    elif engagement_score >= 10:

        level = "moderate"

    else:

        level = "relatively low"

    return (
        f"Learning engagement is {level}, with "
        f"{active_days:.0f} active learning days and "
        f"{resources:.0f} unique learning resources accessed."
    )


# ---------------------------------------------------------
# PRIORITY DETERMINATION
# ---------------------------------------------------------

def determine_unified_priority(
    performance: Dict,
    engagement: Dict,
    trend: Dict,
    weakness_analysis: Dict
) -> Dict:

    average_score = safe_float(
        performance.get("average_score")
    )

    engagement_score = safe_float(
        engagement.get("engagement_score")
    )

    trend_type = trend.get(
        "trend",
        "Unknown"
    )

    weak_count = int(
        weakness_analysis.get(
            "weak_assessment_count",
            0
        )
    )

    reasons: List[str] = []

    # ---------------------------------------------
    # HIGH PRIORITY CONDITIONS
    # ---------------------------------------------

    if average_score < 50:

        reasons.append(
            "Academic performance is currently low"
        )

    if trend_type == "Declining":

        reasons.append(
            "Recent academic performance is declining"
        )

    if weak_count >= 2:

        reasons.append(
            "Multiple assessments require improvement"
        )

    if engagement_score < 5:

        reasons.append(
            "Learning engagement is very low"
        )

    if reasons:

        return {
            "priority": "High",
            "reasons": reasons
        }

    # ---------------------------------------------
    # MEDIUM PRIORITY CONDITIONS
    # ---------------------------------------------

    if average_score < 65:

        reasons.append(
            "Academic performance needs improvement"
        )

    if weak_count == 1:

        reasons.append(
            "One assessment requires attention"
        )

    if engagement_score < 10:

        reasons.append(
            "Learning engagement could be improved"
        )

    if reasons:

        return {
            "priority": "Medium",
            "reasons": reasons
        }

    # ---------------------------------------------
    # LOW PRIORITY
    # ---------------------------------------------

    return {
        "priority": "Low",
        "reasons": [
            "Academic performance is currently stable"
        ]
    }


# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------

def generate_recommendations(
    performance: Dict,
    engagement: Dict,
    trend: Dict,
    weakness_analysis: Dict
) -> List[str]:

    recommendations: List[str] = []

    average_score = safe_float(
        performance.get("average_score")
    )

    engagement_score = safe_float(
        engagement.get("engagement_score")
    )

    trend_type = trend.get(
        "trend",
        "Unknown"
    )

    weak_count = int(
        weakness_analysis.get(
            "weak_assessment_count",
            0
        )
    )

    # Academic performance
    if average_score < 50:

        recommendations.append(
            "Focus on foundational concepts and seek additional academic support."
        )

    elif average_score < 65:

        recommendations.append(
            "Increase revision and practice for upcoming assessments."
        )

    elif average_score >= 80:

        recommendations.append(
            "Maintain the current academic performance while targeting further improvement."
        )

    # Weak assessments
    if weak_count >= 2:

        recommendations.append(
            "Review low-scoring assessments and identify the concepts that caused difficulty."
        )

    elif weak_count == 1:

        recommendations.append(
            "Review the low-scoring assessment and strengthen the related concepts."
        )

    # Engagement
    if engagement_score < 5:

        recommendations.append(
            "Increase regular learning activity and resource usage."
        )

    elif engagement_score < 10:

        recommendations.append(
            "Increase learning engagement through more regular study sessions and resource usage."
        )

    # Trend
    if trend_type == "Declining":

        recommendations.append(
            "Monitor upcoming assessment performance closely and intervene early."
        )

    elif trend_type == "Improving":

        recommendations.append(
            "Continue the current learning strategy because performance is showing improvement."
        )

    # Fallback
    if not recommendations:

        recommendations.append(
            "Continue monitoring academic performance and learning engagement."
        )

    return recommendations


# ---------------------------------------------------------
# UNIFIED ACADEMIC INSIGHT
# ---------------------------------------------------------

def generate_academic_insights(
    intelligence: Dict
) -> Optional[Dict]:

    if not intelligence:

        return None

    performance = intelligence.get(
        "performance",
        {}
    )

    engagement = intelligence.get(
        "engagement",
        {}
    )

    trend = intelligence.get(
        "trend",
        {}
    )

    weakness_analysis = intelligence.get(
        "weakness_analysis",
        {}
    )

    performance_insight = (
        generate_performance_insight(
            performance
        )
    )

    consistency_insight = (
        generate_consistency_insight(
            weakness_analysis
        )
    )

    trend_insight = (
        generate_trend_insight(
            trend
        )
    )

    weakness_insight = (
        generate_weakness_insight(
            weakness_analysis
        )
    )

    engagement_insight = (
        generate_engagement_insight(
            engagement
        )
    )

    unified_priority = (
        determine_unified_priority(
            performance,
            engagement,
            trend,
            weakness_analysis
        )
    )

    recommendations = (
        generate_recommendations(
            performance,
            engagement,
            trend,
            weakness_analysis
        )
    )

    return {

        "summary": performance_insight,

        "performance_insight": (
            performance_insight
        ),

        "consistency_insight": (
            consistency_insight
        ),

        "trend_insight": (
            trend_insight
        ),

        "weakness_insight": (
            weakness_insight
        ),

        "engagement_insight": (
            engagement_insight
        ),

        "priority": unified_priority,

        "recommendations": recommendations
    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    from student_intelligence import (
        get_student_intelligence
    )

    student_id = 11391

    intelligence = (
        get_student_intelligence(
            student_id
        )
    )

    insights = generate_academic_insights(
        intelligence
    )

    print(
        "\n===================================="
    )

    print(
        " EDUASSIST UNIFIED ACADEMIC INSIGHTS"
    )

    print(
        "===================================="
    )

    print(
        f"\nStudent ID: {student_id}"
    )

    print(
        "\nSummary:"
    )

    print(
        insights["summary"]
    )

    print(
        "\nPerformance Insight:"
    )

    print(
        insights["performance_insight"]
    )

    print(
        "\nConsistency Insight:"
    )

    print(
        insights["consistency_insight"]
    )

    print(
        "\nTrend Insight:"
    )

    print(
        insights["trend_insight"]
    )

    print(
        "\nWeakness Insight:"
    )

    print(
        insights["weakness_insight"]
    )

    print(
        "\nEngagement Insight:"
    )

    print(
        insights["engagement_insight"]
    )

    print(
        "\nUnified Priority:"
    )

    print(
        insights["priority"]
    )

    print(
        "\nRecommendations:"
    )

    for recommendation in insights[
        "recommendations"
    ]:

        print(
            f"- {recommendation}"
        )