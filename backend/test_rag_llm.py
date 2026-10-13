"""
EduAssist AI - AI Orchestrator

Central orchestration layer that connects:

    Student Question
            ↓
      NLP Intent Engine
            ↓
    Student Intelligence
            ↓
    Academic Insights
            ↓
       RAG Retrieval
            ↓
       LLM Response
            ↓
    Personalized AI Answer
"""

from typing import Any, Dict

from student_intelligence import (
    get_student_intelligence
)

from academic_insights import (
    generate_academic_insights
)

from intent_engine import (
    analyze_question
)

from rag_engine import (
    build_rag_context
)

from llm_engine import (
    generate_response
)


# ============================================================
# INTENT → REQUIRED STUDENT DATA
# ============================================================

INTENT_DATA_REQUIREMENTS = {

    "PERFORMANCE_ANALYSIS": [
        "performance"
    ],

    "FUTURE_SCORE_PREDICTION": [
        "ml_context",
        "performance",
        "engagement"
    ],

    "RISK_ANALYSIS": [
        "ml_context",
        "performance",
        "engagement"
    ],

    "ENGAGEMENT_ANALYSIS": [
        "engagement"
    ],

    "WEAKNESS_ANALYSIS": [
        "weakness_analysis",
        "performance"
    ],

    "TREND_ANALYSIS": [
        "trend",
        "performance"
    ],

    "OVERALL_ANALYSIS": [
        "performance",
        "assessment_analysis",
        "engagement",
        "trend",
        "weakness_analysis",
        "academic_priority"
    ],

    "RECOMMENDATION": [
        "performance",
        "engagement",
        "trend",
        "weakness_analysis",
        "academic_priority"
    ],

    "STUDY_PLAN": [
        "performance",
        "engagement",
        "trend",
        "weakness_analysis",
        "academic_priority"
    ],

    "GENERAL_ACADEMIC": [],

    "UNKNOWN": []
}


# ============================================================
# CLEAN CONTEXT VALUES
# ============================================================

def clean_context_value(value: Any) -> Any:
    """
    Clean context values before sending them to the LLM.
    """

    if value is None:
        return None

    if isinstance(value, float):

        if value != value:
            return None

        return round(value, 4)

    if isinstance(value, dict):

        return {
            key: clean_context_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):

        return [
            clean_context_value(item)
            for item in value
        ]

    return value


# ============================================================
# BUILD STUDENT CONTEXT
# ============================================================

def build_student_context(
    student_id: int,
    required_fields: list
) -> Dict[str, Any]:
    """
    Build student-specific context required
    for the detected intent.
    """

    intelligence = get_student_intelligence(
        student_id
    )

    if intelligence is None:

        raise ValueError(
            f"Student {student_id} not found."
        )

    context = {
        "student_id": student_id
    }

    # Add required intelligence fields
    for field in required_fields:

        if field in intelligence:

            context[field] = intelligence[field]

    # Generate academic insights when required
    if any(
        field in required_fields
        for field in [
            "academic_priority",
            "weakness_analysis"
        ]
    ):

        insights = generate_academic_insights(
            intelligence
        )

        context["academic_insights"] = insights

    # Add unified academic priority
    if "academic_priority" in required_fields:

        insights = context.get(
            "academic_insights"
        )

        if insights:

            context["academic_priority"] = (
                insights.get("priority")
            )

    return clean_context_value(
        context
    )


# ============================================================
# BUILD COMPLETE RESPONSE CONTEXT
# ============================================================

def build_response_context(
    student_id: int,
    question: str,
    intent_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build the complete context required
    by the LLM.
    """

    intent = intent_result["intent"]

    confidence = intent_result["confidence"]

    required_fields = (
        INTENT_DATA_REQUIREMENTS.get(
            intent,
            []
        )
    )

    # Student intelligence
    student_context = build_student_context(
        student_id,
        required_fields
    )

    # RAG knowledge retrieval
    rag_context = build_rag_context(
        question=question,
        k=3
    )

    return {

        "student_id": student_id,

        "user_question": question,

        "intent": intent,

        "intent_confidence": confidence,

        "required_data": required_fields,

        "student_context": student_context,

        "rag_context": rag_context
    }


# ============================================================
# GENERATE FINAL AI RESPONSE
# ============================================================

def generate_ai_response(
    response_context: Dict[str, Any]
) -> str:
    """
    Generate final personalized response using:

        Student Intelligence
                +
        RAG Knowledge
                +
        LLM
    """

    question = response_context[
        "user_question"
    ]

    intent = response_context[
        "intent"
    ]

    student_context = response_context[
        "student_context"
    ]

    rag_context = response_context[
        "rag_context"
    ]

    # --------------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------------

    system_prompt = """
You are EduAssist AI, a personalized academic
assistant for college students.

Your role is to provide accurate, useful,
student-specific academic guidance.

You may receive:

1. Student Intelligence
2. Academic Insights
3. Retrieved academic knowledge
4. Student question
5. Detected intent

IMPORTANT RULES:

- Use student data when answering personalized questions.
- Use retrieved academic knowledge when it is available.
- Do not invent student information.
- Do not invent academic facts when retrieved knowledge
  is provided.
- If no relevant academic knowledge was retrieved,
  do not pretend that a knowledge-base source exists.
- Never claim that OULAD contains subject-specific marks
  when it does not.
- Do not mention internal technical details such as
  FAISS, embeddings, vector stores, similarity distances,
  or orchestration unless the student asks about them.
- Keep answers clear and useful for college students.
- For recommendations and study plans, personalize the
  answer using the student's actual performance, trend,
  weaknesses, and engagement.
- Do not unnecessarily repeat raw numerical data.
- If the available student data is insufficient, clearly
  mention the limitation.
"""

    # --------------------------------------------------------
    # USER PROMPT
    # --------------------------------------------------------

    prompt = f"""
Student Question:
{question}

Detected Intent:
{intent}

Student Intelligence:
{student_context}

Retrieved Academic Knowledge:
{rag_context.get("context", "")}

Retrieval Status:
{rag_context.get("retrieval_status", "unknown")}

Generate the final answer for the student.

For personalized questions:
Use the student's actual intelligence and insights.

For academic questions:
Use retrieved academic knowledge when available.

Make the answer clear, concise, accurate,
and personalized where possible.
"""

    # --------------------------------------------------------
    # CALL LOCAL LLM
    # --------------------------------------------------------

    return generate_response(
        prompt=prompt,
        system_prompt=system_prompt
    )


# ============================================================
# COMPLETE ORCHESTRATION PIPELINE
# ============================================================

def orchestrate_question(
    student_id: int,
    question: str
) -> Dict[str, Any]:
    """
    Complete EduAssist AI pipeline:

        Student Question
                ↓
        NLP Intent Detection
                ↓
        Student Intelligence
                ↓
        RAG Retrieval
                ↓
        Local LLM
                ↓
        Personalized Response
    """

    # STEP 1 — NLP Intent Detection
    intent_result = analyze_question(
        question
    )

    # STEP 2 — Build Student + RAG Context
    response_context = build_response_context(
        student_id,
        question,
        intent_result
    )

    # STEP 3 — Generate LLM Response
    ai_response = generate_ai_response(
        response_context
    )

    # STEP 4 — Attach final response
    response_context[
        "ai_response"
    ] = ai_response

    return response_context


# ============================================================
# TEST
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

        "What is normalization in DBMS?"
    ]

    for question in test_questions:

        print("\n" + "=" * 70)

        print(
            "QUESTION:",
            question
        )

        try:

            result = orchestrate_question(
                test_student_id,
                question
            )

            print(
                "INTENT:",
                result["intent"]
            )

            print(
                "CONFIDENCE:",
                result["intent_confidence"]
            )

            print(
                "RAG STATUS:",
                result["rag_context"][
                    "retrieval_status"
                ]
            )

            print(
                "\nAI RESPONSE:"
            )

            print(
                result["ai_response"]
            )

        except Exception as error:

            print(
                "\nERROR:",
                error
            )