
import logging
import math
import time
from typing import Any, Dict, List

from .student_intelligence import get_student_intelligence
from .academic_insights import generate_academic_insights
from .rag_engine import build_rag_context
from .llm_engine import generate_response
from .intent_engine import analyze_question

logger = logging.getLogger("eduassist.orchestrator")




# ============================================================
# DATA REQUIREMENTS BY INTENT
# ============================================================

INTENT_DATA_REQUIREMENTS: Dict[str, List[str]] = {
    "PERFORMANCE_ANALYSIS": [
        "performance",
    ],
    "FUTURE_SCORE_PREDICTION": [
        "ml_context",
        "performance",
        "engagement",
    ],
    "RISK_ANALYSIS": [
        "ml_context",
        "performance",
        "engagement",
    ],
    "ENGAGEMENT_ANALYSIS": [
        "engagement",
    ],
    "WEAKNESS_ANALYSIS": [
        "weakness_analysis",
        "performance",
    ],
    "TREND_ANALYSIS": [
        "trend",
        "performance",
    ],
    "OVERALL_ANALYSIS": [
        "performance",
        "assessment_analysis",
        "engagement",
        "trend",
        "weakness_analysis",
        "academic_priority",
    ],
    "RECOMMENDATION": [
        "performance",
        "engagement",
        "trend",
        "weakness_analysis",
        "academic_priority",
    ],
    "STUDY_PLAN": [
        "performance",
        "engagement",
        "trend",
        "weakness_analysis",
        "academic_priority",
    ],
    "GENERAL_ACADEMIC": [],
    "UNKNOWN": [],
}


# ============================================================
# CONTEXT CLEANING
# ============================================================

def clean_context_value(value: Any) -> Any:
    """
    Convert nested values into safe, prompt-friendly values.

    Handles dictionaries, lists, numpy scalars, NaN, and infinity.
    """

    if isinstance(value, dict):
        return {
            str(key): clean_context_value(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            clean_context_value(item)
            for item in value
        ]

    if value is None:
        return None

    if hasattr(value, "item"):
        try:
            value = value.item()
        except (ValueError, TypeError):
            pass

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return round(value, 4)

    return value


# ============================================================
# BUILD STUDENT CONTEXT
# ============================================================

def build_student_context(
    student_id: int,
    required_fields: List[str],
) -> Dict[str, Any]:
    started = time.perf_counter()

    logger.info(
        "Student context started: student_id=%s fields=%s",
        student_id,
        required_fields,
    )

    intelligence = get_student_intelligence(student_id)

    if not isinstance(intelligence, dict):
        raise TypeError(
            "get_student_intelligence() must return a dictionary"
        )

    student_context: Dict[str, Any] = {}

    # Select the fields required by the detected intent.
    for field in required_fields:
        if field in intelligence:
            student_context[field] = intelligence[field]

    # Generate academic insights only when the intent needs them.
    needs_insights = any(
        field in required_fields
        for field in (
            "academic_priority",
            "weakness_analysis",
        )
    )

    if needs_insights:
        insights_started = time.perf_counter()

        insights = generate_academic_insights(intelligence)

        logger.info(
            "Academic insights completed in %.3fs",
            time.perf_counter() - insights_started,
        )

        if isinstance(insights, dict):
            student_context["academic_insights"] = insights

            if "academic_priority" in required_fields:
                if "academic_priority" in insights:
                    student_context["academic_priority"] = (
                        insights["academic_priority"]
                    )
                elif "priorities" in insights:
                    student_context["academic_priority"] = (
                        insights["priorities"]
                    )

            if (
                "weakness_analysis" in required_fields
                and "weakness_analysis" not in student_context
            ):
                if "weakness_analysis" in insights:
                    student_context["weakness_analysis"] = (
                        insights["weakness_analysis"]
                    )
                elif "weak_areas" in insights:
                    student_context["weakness_analysis"] = (
                        insights["weak_areas"]
                    )

    cleaned_context = clean_context_value(student_context)

    logger.info(
        "Student context completed: student_id=%s duration=%.3fs",
        student_id,
        time.perf_counter() - started,
    )

    return cleaned_context


# ============================================================
# BUILD FULL RESPONSE CONTEXT
# ============================================================


def build_response_context(
    student_id: int,
    question: str,
    intent_result: Dict[str, Any],
) -> Dict[str, Any]:
    started = time.perf_counter()

    intent = str(
        intent_result.get("intent", "UNKNOWN")
    ).upper()

    confidence = intent_result.get(
        "confidence",
        intent_result.get("intent_confidence"),
    )

    required_fields = INTENT_DATA_REQUIREMENTS.get(
        intent,
        [],
    )

    # Load student intelligence only when this intent needs it.
    if required_fields:
        student_context = build_student_context(
            student_id=student_id,
            required_fields=required_fields,
        )
    else:
        student_context = {}

    # Retrieve knowledge for general academic questions.
    rag_started = time.perf_counter()

    logger.info(
        "RAG retrieval started: student_id=%s intent=%s",
        student_id,
        intent,
    )

    rag_context = build_rag_context(
        question=question,
        k=3,
    )

    logger.info(
        "RAG retrieval completed: duration=%.3fs",
        time.perf_counter() - rag_started,
    )

    # Keep only the retrieved text when the result is a dictionary.
    # This avoids sending duplicate source metadata to the LLM.
    if isinstance(rag_context, dict):
        compact_rag_context = rag_context.get(
            "context",
            rag_context,
        )
    else:
        compact_rag_context = rag_context

    # Limit the knowledge text included in the prompt.
    if isinstance(compact_rag_context, str):
        compact_rag_context = compact_rag_context[:10000]

    result = {
        "student_id": student_id,
        "user_question": question,
        "intent": intent,
        "intent_confidence": confidence,
        "required_data": required_fields,
        "student_context": student_context,
        "rag_context": clean_context_value(
            compact_rag_context
        ),
    }

    logger.info(
        "Response context completed: student_id=%s duration=%.3fs",
        student_id,
        time.perf_counter() - started,
    )

    return result


# ============================================================
# OLLAMA RESPONSE GENERATION
# ============================================================

def generate_ai_response(context: Dict[str, Any]) -> str:
    """
    Generate the answer through the existing Ollama service.

    The prompt includes student context and retrieved RAG knowledge.
    """

    system_prompt = """
You are EduAssist AI, a helpful personal academic assistant.

Your purpose is to help students understand academic concepts,
interpret their available academic data, identify improvement areas,
and create practical study plans.

Rules:
1. Answer the student's actual question directly.
2. Use retrieved RAG knowledge when it is relevant.
3. Use supplied student data for student-specific questions.
4. Never invent scores, predictions, records, or retrieved facts.
5. If required information is missing, clearly say so.
6. Explain concepts in clear, student-friendly language.
7. Make recommendations specific and actionable.
8. Treat future-score predictions as estimates, not guarantees.
9. Do not claim that an action or analysis was performed if it was not.
10. Avoid repeating the entire context in your response.
""".strip()

    user_prompt = f"""
Student ID:
{context.get("student_id")}

Detected intent:
{context.get("intent")}

Intent confidence:
{context.get("intent_confidence")}

Student question:
{context.get("user_question")}

Relevant student context:
{context.get("student_context", {})}

Retrieved RAG context:
{context.get("rag_context", {})}

Instructions:
Answer the student's question directly.

For academic concept questions, explain the concept using relevant
retrieved knowledge.

For student-specific questions, rely on the supplied student context
and do not invent missing academic records.

For recommendations or study plans, provide practical next steps.
If the supplied information is insufficient, acknowledge the limitation.
""".strip()

    started = time.perf_counter()

    logger.info(
        "Ollama generation started: student_id=%s intent=%s",
        context.get("student_id"),
        context.get("intent"),
    )

    try:
        # Keep this call aligned with the existing llm_service.py.
        answer = generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        if answer is None:
            answer = ""

        if not isinstance(answer, str):
            answer = str(answer)

        answer = answer.strip()

        logger.info(
            "Ollama generation completed: duration=%.3fs answer_chars=%s",
            time.perf_counter() - started,
            len(answer),
        )

        if not answer:
            logger.warning(
                "Ollama returned an empty answer for student %s",
                context.get("student_id"),
            )

        return answer

    except Exception:
        logger.exception(
            "Ollama generation failed after %.3fs",
            time.perf_counter() - started,
        )
        raise


# ============================================================
# MAIN ORCHESTRATOR
# ============================================================

def orchestrate_question(
    student_id: int,
    question: str,
) -> Dict[str, Any]:
    """
    Execute the full pipeline for EVERY question:

        1. Intent detection
        2. Student context
        3. Academic insights when required
        4. RAG retrieval
        5. Ollama response generation

    Stage timings are written to the backend terminal.
    """

    total_started = time.perf_counter()

    logger.info(
        "Orchestration started: student_id=%s question_chars=%s",
        student_id,
        len(question or ""),
    )

    try:
        # ----------------------------------------------------
        # Stage 1: intent detection
        # ----------------------------------------------------
        intent_started = time.perf_counter()

        intent_result = analyze_question(question)

        logger.info(
            "Intent detection completed in %.3fs: %s",
            time.perf_counter() - intent_started,
            intent_result,
        )

        if not isinstance(intent_result, dict):
            raise TypeError(
                "analyze_question() must return a dictionary"
            )

        # ----------------------------------------------------
        # Stages 2 and 3: student context + RAG
        # ----------------------------------------------------
        context = build_response_context(
            student_id=student_id,
            question=question,
            intent_result=intent_result,
        )

        # ----------------------------------------------------
        # Stage 4: Ollama response generation
        # ----------------------------------------------------
        # Intentionally runs for every intent, including
        # performance, trend, recommendation, and study plan.
        context["ai_response"] = generate_ai_response(context)

        # ----------------------------------------------------
        # Final result
        # ----------------------------------------------------
        logger.info(
            "Orchestration completed: student_id=%s intent=%s total=%.3fs",
            student_id,
            context.get("intent"),
            time.perf_counter() - total_started,
        )

        return context

    except Exception:
        logger.exception(
            "Orchestration failed: student_id=%s elapsed=%.3fs",
            student_id,
            time.perf_counter() - total_started,
        )
        raise


# ============================================================
# OPTIONAL MANUAL TEST
# Run this file as a module from the correct package context.
# ============================================================

if __name__ == "__main__":
    test_student_id = 11391

    test_questions = [
        "What is my current performance?",
        "What are my weak areas?",
        "Am I improving?",
        "How can I improve my performance?",
        "Give me an overall analysis",
        "Create a study plan for me",
        "Explain object-oriented programming",
        "What is overfitting in machine learning?",
        "How can I prepare for my next assessment?",
    ]

    for test_question in test_questions:
        print(f"\nQuestion: {test_question}")

        try:
            result = orchestrate_question(
                student_id=test_student_id,
                question=test_question,
            )

            print("Intent:", result.get("intent"))
            print("Answer:", result.get("ai_response"))

        except Exception as error:
            print(f"Request failed: {error}")
