import re
from typing import Dict, List


# =========================================================
# INTENT DEFINITIONS
# =========================================================

INTENTS = {

    "PERFORMANCE_ANALYSIS": {
        "description": (
            "Questions about current academic performance, "
            "marks, scores, average, highest or lowest score."
        )
    },

    "FUTURE_SCORE_PREDICTION": {
        "description": (
            "Questions asking about predicted future score "
            "or expected academic performance."
        )
    },

    "RISK_ANALYSIS": {
        "description": (
            "Questions about academic risk, failure risk, "
            "or whether the student is at risk."
        )
    },

    "ENGAGEMENT_ANALYSIS": {
        "description": (
            "Questions about learning activity, engagement, "
            "active days, resource usage or study activity."
        )
    },

    "WEAKNESS_ANALYSIS": {
        "description": (
            "Questions about weak areas, weak assessments, "
            "strengths, consistency or difficult areas."
        )
    },

    "TREND_ANALYSIS": {
        "description": (
            "Questions about improvement, decline, progress "
            "or academic performance trend."
        )
    },

    "OVERALL_ANALYSIS": {
        "description": (
            "Questions asking for a complete analysis of "
            "the student's academic condition."
        )
    },

    "RECOMMENDATION": {
        "description": (
            "Questions asking what the student should do, "
            "how to improve, or what actions to take."
        )
    },

    "STUDY_PLAN": {
        "description": (
            "Questions asking for a study plan, schedule, "
            "revision plan or personalized study routine."
        )
    },

    "GENERAL_ACADEMIC": {
        "description": (
            "General academic questions that do not require "
            "student-specific intelligence."
        )
    },

    "UNKNOWN": {
        "description": (
            "Question does not match a supported intent."
        )
    }
}


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text: str) -> str:
    """
    Normalize user question before intent detection.
    """

    if not text:
        return ""

    text = text.lower().strip()

    text = re.sub(
        r"[^a-z0-9\s%]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# =========================================================
# KEYWORD GROUPS
# =========================================================

PERFORMANCE_KEYWORDS = [
    "performance",
    "marks",
    "mark",
    "score",
    "scores",
    "average",
    "average score",
    "current performance",
    "my performance",
    "academic performance",
    "highest score",
    "lowest score"
]


FUTURE_SCORE_KEYWORDS = [
    "future score",
    "predicted score",
    "predict my score",
    "expected score",
    "expected marks",
    "future performance",
    "predict performance",
    "what will i score",
    "how much will i score",
    "forecast my score"
]


RISK_KEYWORDS = [
    "risk",
    "at risk",
    "academic risk",
    "failure risk",
    "fail",
    "failing",
    "danger"
]


ENGAGEMENT_KEYWORDS = [
    "engagement",
    "learning activity",
    "activity",
    "active days",
    "learning days",
    "resources",
    "resource usage",
    "clicks",
    "vle",
    "study activity",
    "how active"
]


WEAKNESS_KEYWORDS = [
    "weakness",
    "weak",
    "weak areas",
    "weak area",
    "weak subjects",
    "weak subject",
    "difficult areas",
    "difficulty",
    "strengths",
    "strong areas",
    "consistency",
    "consistent",
    "inconsistent",
    "where am i weak"
]


TREND_KEYWORDS = [
    "trend",
    "progress",
    "improving",
    "improvement",
    "declining",
    "decline",
    "getting better",
    "getting worse",
    "performance trend",
    "am i improving",
    "how am i progressing"
]


OVERALL_KEYWORDS = [
    "overall",
    "overall analysis",
    "analyze me",
    "analyse me",
    "analyze my performance",
    "analyse my performance",
    "how am i doing",
    "how am i performing",
    "complete analysis",
    "full analysis",
    "academic analysis",
    "student analysis",
    "give me my analysis"
]


RECOMMENDATION_KEYWORDS = [
    "recommend",
    "recommendation",
    "recommendations",
    "what should i do",
    "what should i improve",
    "how can i improve",
    "how do i improve",
    "how to improve",
    "improve my performance",
    "help me improve",
    "what can i do",
    "suggest",
    "suggestions",
    "advice",
    "what should i focus on"
]


STUDY_PLAN_KEYWORDS = [
    "study plan",
    "study schedule",
    "study routine",
    "study timetable",
    "revision plan",
    "revision schedule",
    "learning plan",
    "personalized plan",
    "personalised plan",
    "make a plan",
    "create a plan",
    "plan my study",
    "schedule my study",
    "how should i study"
]


GENERAL_ACADEMIC_KEYWORDS = [
    "explain",
    "define",
    "what is",
    "meaning",
    "difference between",
    "how does",
    "why does",
    "concept",
    "topic"
]


# =========================================================
# KEYWORD MATCHING
# =========================================================

def keyword_matches(
    text: str,
    keywords: List[str]
) -> List[str]:

    matches = []

    for keyword in keywords:

        if keyword in text:

            matches.append(
                keyword
            )

    return matches


# =========================================================
# INTENT SCORING
# =========================================================

def calculate_intent_scores(
    text: str
) -> Dict[str, Dict]:

    intent_groups = {

        "PERFORMANCE_ANALYSIS":
            PERFORMANCE_KEYWORDS,

        "FUTURE_SCORE_PREDICTION":
            FUTURE_SCORE_KEYWORDS,

        "RISK_ANALYSIS":
            RISK_KEYWORDS,

        "ENGAGEMENT_ANALYSIS":
            ENGAGEMENT_KEYWORDS,

        "WEAKNESS_ANALYSIS":
            WEAKNESS_KEYWORDS,

        "TREND_ANALYSIS":
            TREND_KEYWORDS,

        "OVERALL_ANALYSIS":
            OVERALL_KEYWORDS,

        "RECOMMENDATION":
            RECOMMENDATION_KEYWORDS,

        "STUDY_PLAN":
            STUDY_PLAN_KEYWORDS,

        "GENERAL_ACADEMIC":
            GENERAL_ACADEMIC_KEYWORDS
    }

    scores = {}

    for intent, keywords in intent_groups.items():

        matches = keyword_matches(
            text,
            keywords
        )

        score = len(matches)

        scores[intent] = {
            "score": score,
            "matched_keywords": matches
        }

    return scores


# =========================================================
# INTENT PRIORITY
# =========================================================

INTENT_PRIORITY = {

    "STUDY_PLAN": 10,

    "FUTURE_SCORE_PREDICTION": 9,

    "RISK_ANALYSIS": 8,

    "OVERALL_ANALYSIS": 7,

    "RECOMMENDATION": 6,

    "WEAKNESS_ANALYSIS": 5,

    "TREND_ANALYSIS": 4,

    "ENGAGEMENT_ANALYSIS": 3,

    "PERFORMANCE_ANALYSIS": 2,

    "GENERAL_ACADEMIC": 1
}


# =========================================================
# MAIN INTENT DETECTOR
# =========================================================

def detect_intent(
    question: str
) -> Dict:

    normalized_question = normalize_text(
        question
    )

    if not normalized_question:

        return {
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "matched_keywords": [],
            "scores": {}
        }

    scores = calculate_intent_scores(
        normalized_question
    )

    # -----------------------------------------------------
    # SORT BY SCORE
    # -----------------------------------------------------

    ranked_intents = sorted(
        scores.items(),
        key=lambda item: (
            item[1]["score"],
            INTENT_PRIORITY.get(
                item[0],
                0
            )
        ),
        reverse=True
    )

    best_intent = ranked_intents[0][0]

    best_score = ranked_intents[0][1]["score"]

    second_score = (
        ranked_intents[1][1]["score"]
        if len(ranked_intents) > 1
        else 0
    )

    # -----------------------------------------------------
    # UNKNOWN
    # -----------------------------------------------------

    if best_score == 0:

        return {
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "matched_keywords": [],
            "scores": scores
        }

    # -----------------------------------------------------
    # CONFIDENCE
    # -----------------------------------------------------

    total_score = sum(
        item["score"]
        for item in scores.values()
    )

    if total_score == 0:

        confidence = 0.0

    else:

        confidence = (
            best_score / total_score
        )

    # -----------------------------------------------------
    # AMBIGUITY HANDLING
    # -----------------------------------------------------

    if (
        best_score == second_score
        and best_score == 1
    ):

        confidence = 0.5

    elif (
        best_score > second_score
        and best_score >= 2
    ):

        confidence = min(
            0.95,
            0.5 + (
                best_score - second_score
            ) * 0.15
        )

    else:

        confidence = min(
            0.9,
            confidence
        )

    return {
        "intent": best_intent,
        "confidence": round(
            confidence,
            3
        ),
        "matched_keywords": (
            scores[best_intent][
                "matched_keywords"
            ]
        ),
        "scores": scores
    }


# =========================================================
# INTENT DESCRIPTION
# =========================================================

def get_intent_description(
    intent: str
) -> str:

    return INTENTS.get(
        intent,
        INTENTS["UNKNOWN"]
    )["description"]


# =========================================================
# COMPLETE INTENT ANALYSIS
# =========================================================

def analyze_question(
    question: str
) -> Dict:

    result = detect_intent(
        question
    )

    intent = result[
        "intent"
    ]

    return {
        "question": question,
        "normalized_question": normalize_text(
            question
        ),
        "intent": intent,
        "intent_description": (
            get_intent_description(
                intent
            )
        ),
        "confidence": result[
            "confidence"
        ],
        "matched_keywords": result[
            "matched_keywords"
        ],
        "scores": result[
            "scores"
        ]
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    test_questions = [

        "What is my current performance?",

        "What is my predicted future score?",

        "Am I at academic risk?",

        "How is my learning engagement?",

        "What are my weak areas?",

        "Am I improving?",

        "Give me an overall analysis",

        "How can I improve my performance?",

        "Create a study plan for me",

        "What is machine learning?"
    ]

    print(
        "\n=========================================="
    )

    print(
        " EDUASSIST AI - NLP INTENT ENGINE"
    )

    print(
        "=========================================="
    )

    for question in test_questions:

        result = analyze_question(
            question
        )

        print(
            "\n------------------------------------------"
        )

        print(
            f"Question: {question}"
        )

        print(
            f"Intent: {result['intent']}"
        )

        print(
            f"Confidence: {result['confidence']}"
        )

        print(
            "Matched keywords:",
            result["matched_keywords"]
        )