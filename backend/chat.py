
from typing import Any, Callable, Dict, Optional

from .student_intelligence import get_student_intelligence
from .ai_orchestrator import orchestrate_question
from .intent_engine import analyze_question


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def number(value: Any, suffix: str = "") -> str:
    """Format numeric values safely without duplicating suffixes."""
    if value is None:
        return "Not available"

    try:
        formatted = f"{float(value):.2f}".rstrip("0").rstrip(".")
        return formatted + suffix
    except (TypeError, ValueError):
        return str(value)


def get_intent(question: str) -> Dict[str, Any]:
    """Safely read the intent detector's result."""
    result = analyze_question(question)

    if isinstance(result, dict):
        return {
            "intent": str(result.get("intent", "UNKNOWN")).upper(),
            "confidence": result.get(
                "intent_confidence",
                result.get("confidence"),
            ),
        }

    return {
        "intent": str(result).upper(),
        "confidence": None,
    }


def format_performance(data: Dict[str, Any]) -> str:
    average = data.get("average_score")
    count = data.get("assessment_count", 0)
    highest = data.get("highest_score")
    lowest = data.get("lowest_score")
    category = data.get("performance_category") or "Not available"

    return (
        f"Your average score is {number(average, '%')} across "
        f"{count} assessments. Your highest score is "
        f"{number(highest, '%')} and your lowest score is "
        f"{number(lowest, '%')}. Your current performance category "
        f"is {category}."
    )


def format_engagement(data: Dict[str, Any]) -> str:
    return (
        f"You recorded {data.get('total_clicks', 0)} learning-platform "
        f"clicks across {data.get('active_days', 0)} active days. "
        f"Your engagement score is {number(data.get('engagement_score'))}, "
        f"and you accessed {data.get('unique_vle_resources', 0)} "
        f"unique learning resources."
    )


def format_weakness(data: Optional[Dict[str, Any]]) -> str:
    if not data:
        return (
            "There is insufficient assessment data to identify "
            "your weak areas."
        )

    weak_count = data.get("weak_assessment_count", 0)
    assessment_count = data.get("assessment_count", 0)
    average = data.get("average_score")
    lowest = data.get("lowest_score")
    trend = str(data.get("trend", "Unknown"))
    consistency = str(data.get("consistency", "Unknown"))

    parts = [
        f"You have {weak_count} assessment(s) below 65 out of "
        f"{assessment_count} recorded assessments."
    ]

    if average is not None:
        parts.append(f"Your average score is {number(average, '%')}.")

    # number() already appends the percentage symbol.
    if lowest is not None:
        parts.append(f"Your lowest score is {number(lowest, '%')}.")

    parts.append(
        f"Your performance trend is {trend.lower()}, and your "
        f"scores are {consistency.lower()}."
    )

    type_analysis = data.get("assessment_type_analysis") or []

    valid_types = [
        item for item in type_analysis
        if item.get("average_score") is not None
    ]

    if valid_types:
        weakest_type = min(
            valid_types,
            key=lambda item: float(item["average_score"]),
        )
        parts.append(
            f"Among the recorded assessment types, "
            f"{weakest_type.get('assessment_type', 'Unknown')} has "
            f"the lowest average at "
            f"{number(weakest_type.get('average_score'), '%')}."
        )

    if weak_count > 0:
        parts.append(
            "Review the low-scoring assessments, identify the concepts "
            "behind your mistakes, and practise similar questions."
        )
    else:
        parts.append(
            "No assessments fall below the 65-point threshold. "
            "Assessment scores alone cannot identify topic-level "
            "weaknesses, so review feedback to find concepts needing "
            "more practice."
        )

    return " ".join(parts)


def format_trend(data: Dict[str, Any]) -> str:
    first = data.get("first_score")
    latest = data.get("latest_score")
    change = data.get("change", data.get("score_change"))
    trend = str(data.get("trend", "Unknown"))

    if first is None or latest is None:
        return f"Your current performance trend is {trend.lower()}."

    try:
        change_value = float(change or 0)
    except (TypeError, ValueError):
        change_value = 0

    if change_value > 0:
        direction = "increased"
    elif change_value < 0:
        direction = "decreased"
    else:
        direction = "remained unchanged"

    return (
        f"Your first recorded score was {number(first, '%')} and your "
        f"latest score was {number(latest, '%')}. Your score "
        f"{direction} by {number(abs(change_value), ' points')}. "
        f"Overall, your trend is {trend.lower()}."
    )


def build_recommendations(intelligence: Dict[str, Any]) -> str:
    performance = intelligence.get("performance") or {}
    engagement = intelligence.get("engagement") or {}
    weakness = intelligence.get("weakness_analysis") or {}
    trend = intelligence.get("trend") or {}

    recommendations = []

    average = performance.get("average_score")
    engagement_score = engagement.get("engagement_score")
    weak_count = weakness.get("weak_assessment_count", 0)
    trend_name = str(trend.get("trend", "")).lower()

    if average is not None and average < 65:
        recommendations.append(
            "Prioritize core concepts and solve practice questions "
            "before attempting another assessment."
        )
    elif average is not None and average < 80:
        recommendations.append(
            "Work toward an 80% average by reviewing incorrect answers "
            "and practising the concepts where you lose marks."
        )
    elif average is not None:
        recommendations.append(
            "Maintain your strong performance with regular revision "
            "and timed practice tests."
        )

    if weak_count > 0:
        recommendations.append(
            f"Review the {weak_count} assessment(s) scoring below 65 "
            "and identify the topics responsible for lost marks."
        )

    if engagement_score is not None and engagement_score < 10:
        recommendations.append(
            "Build a consistent daily learning habit. Study course "
            "materials, complete practice activities, and review "
            "the available learning resources."
        )

    if trend_name == "declining":
        recommendations.append(
            "Review recent coursework and compare recent assessment "
            "feedback to find what may be affecting your scores."
        )
    elif trend_name == "improving":
        recommendations.append(
            "Continue the study habits that are helping your scores "
            "improve and monitor your next assessment."
        )

    if not recommendations:
        recommendations.append(
            "Continue your study routine, practise regularly, and "
            "use assessment feedback to guide your next revision."
        )

    return "Recommended next steps:\n" + "\n".join(
        f"{index}. {item}"
        for index, item in enumerate(recommendations, start=1)
    )


def build_study_plan(intelligence: Dict[str, Any]) -> str:
    performance = intelligence.get("performance") or {}
    weakness = intelligence.get("weakness_analysis") or {}
    engagement = intelligence.get("engagement") or {}

    average = performance.get("average_score")
    weak_count = weakness.get("weak_assessment_count", 0)
    engagement_score = engagement.get("engagement_score")

    starting_point = (
        f"Your current average is {number(average, '%')}."
        if average is not None
        else "Your current average is unavailable."
    )

    tasks = []

    if weak_count > 0:
        tasks.append(
            "Days 1–2: Review low-scoring assessments and list the "
            "concepts behind your mistakes."
        )
    else:
        tasks.append(
            "Days 1–2: Revise recent course material and identify "
            "topics that you find difficult."
        )

    tasks.append(
        "Days 3–4: Practise questions on those topics and review "
        "your answers and feedback."
    )

    if engagement_score is not None and engagement_score < 10:
        tasks.append(
            "Days 5–6: Schedule a daily learning session and use "
            "your course resources or practice activities."
        )
    else:
        tasks.append(
            "Days 5–6: Complete mixed practice questions and revisit "
            "any mistakes."
        )

    tasks.append(
        "Day 7: Take a short self-test, compare your result with "
        "previous scores, and plan the next week's revision."
    )

    return (
        f"{starting_point}\n\nYour 7-day study plan:\n"
        + "\n".join(
            f"{index}. {task}"
            for index, task in enumerate(tasks, start=1)
        )
    )


def format_overall_analysis(
    intelligence: Dict[str, Any],
) -> str:
    """Summarize the student profile without repeating full analyses."""
    performance = intelligence.get("performance") or {}
    engagement = intelligence.get("engagement") or {}
    trend = intelligence.get("trend") or {}
    weakness = intelligence.get("weakness_analysis") or {}
    priority = intelligence.get("academic_priority") or {}

    average = performance.get("average_score")
    latest = trend.get("latest_score")
    first = trend.get("first_score")
    weak_count = weakness.get("weak_assessment_count", 0)
    engagement_score = engagement.get("engagement_score")
    priority_name = priority.get("priority", "Not available")

    parts = ["Overall academic analysis:"]

    if average is not None:
        parts.append(
            f"Your average is {number(average, '%')} across "
            f"{performance.get('assessment_count', 0)} assessments, "
            f"and your performance category is "
            f"{performance.get('performance_category') or 'not available'}."
        )

    if first is not None and latest is not None:
        change = trend.get("change", trend.get("score_change", 0))
        try:
            change = float(change or 0)
        except (TypeError, ValueError):
            change = 0

        direction = (
            "up" if change > 0
            else "down" if change < 0
            else "unchanged"
        )

        parts.append(
            f"Your score trend is {trend.get('trend', 'unknown').lower()}: "
            f"from {number(first, '%')} to {number(latest, '%')}, "
            f"{direction} by {number(abs(change), ' points')}."
        )

    parts.append(
        f"You have {weak_count} assessment(s) below 65. "
        + (
            "Review these assessments to identify concepts to improve."
            if weak_count > 0
            else "No recorded assessments are below 65; use feedback "
                 "to identify any topic-level gaps."
        )
    )

    if engagement_score is not None:
        parts.append(
            f"Your engagement score is {number(engagement_score)}. "
            + (
                "More regular use of learning resources may help."
                if engagement_score < 10
                else "Continue engaging with course resources consistently."
            )
        )

    parts.append(f"Academic priority: {priority_name}.")

    return "\n\n".join(parts)


# ---------------------------------------------------------
# CHAT ROUTER
# ---------------------------------------------------------

def handle_chat(
    student_id: int,
    question: str,
    future_score_handler: Optional[Callable[[int], str]] = None,
    risk_handler: Optional[Callable[[int], str]] = None,
) -> Dict[str, Any]:

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    intent_result = get_intent(question)
    intent = intent_result["intent"]
    confidence = intent_result["confidence"]

    direct_intents = {
        "PERFORMANCE_ANALYSIS",
        "ENGAGEMENT_ANALYSIS",
        "WEAKNESS_ANALYSIS",
        "TREND_ANALYSIS",
        "OVERALL_ANALYSIS",
        "RECOMMENDATION",
        "STUDY_PLAN",
    }

    if intent in direct_intents:
        intelligence = get_student_intelligence(student_id)

        if intelligence is None:
            raise ValueError(f"Student {student_id} was not found.")

        performance = intelligence.get("performance") or {}
        engagement = intelligence.get("engagement") or {}
        trend = intelligence.get("trend") or {}
        weakness = intelligence.get("weakness_analysis") or {}
        priority = intelligence.get("academic_priority") or {}

        if intent == "PERFORMANCE_ANALYSIS":
            response = format_performance(performance)

        elif intent == "ENGAGEMENT_ANALYSIS":
            response = format_engagement(engagement)

        elif intent == "WEAKNESS_ANALYSIS":
            response = format_weakness(weakness)

        elif intent == "TREND_ANALYSIS":
            response = format_trend(trend)

        elif intent == "OVERALL_ANALYSIS":
            response = format_overall_analysis(intelligence)

        elif intent == "RECOMMENDATION":
            response = build_recommendations(intelligence)

        else:
            response = build_study_plan(intelligence)

        return {
            "student_id": student_id,
            "question": question,
            "intent": intent,
            "intent_confidence": confidence,
            "response": response,
            "additional_data": {
                "performance": performance,
                "engagement": engagement,
                "trend": trend,
                "weakness_analysis": weakness,
                "academic_priority": priority,
            },
        }

    if intent == "FUTURE_SCORE_PREDICTION" and future_score_handler:
        return {
            "student_id": student_id,
            "question": question,
            "intent": intent,
            "intent_confidence": confidence,
            "response": future_score_handler(student_id),
        }

    if intent == "RISK_ANALYSIS" and risk_handler:
        return {
            "student_id": student_id,
            "question": question,
            "intent": intent,
            "intent_confidence": confidence,
            "response": risk_handler(student_id),
        }

    # General academic questions continue using the existing RAG + LLM.
    context = orchestrate_question(
        student_id=student_id,
        question=question,
    )

    return {
        "student_id": student_id,
        "question": question,
        "intent": str(context.get("intent", intent)).upper(),
        "intent_confidence": context.get(
            "intent_confidence",
            context.get("confidence", confidence),
        ),
        "response": str(context.get("ai_response", "")).strip()
        or "I couldn't generate a response. Please try again.",
    }
