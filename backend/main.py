
from pathlib import Path

import logging
import time
from typing import Any, Dict

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .student_intelligence import get_student_intelligence
from .academic_insights import generate_academic_insights
from .chat import handle_chat


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("eduassist.api")


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PERFORMANCE_MODEL_PATH = (
    MODELS_DIR / "gradient_boosting_performance_model.pkl"
)

RISK_MODEL_PATH = (
    MODELS_DIR / "risk_classification_model.pkl"
)

STUDENT_DATA_PATH = (
    PROCESSED_DIR / "eduassist_student_dataset.csv"
)

ML_DATA_PATH = (
    PROCESSED_DIR / "eduassist_ml_dataset.csv"
)


# ============================================================
# MODEL FEATURES
# ============================================================

MODEL_FEATURES = [
    "code_module",
    "code_presentation",
    "first_score",
    "second_score",
    "early_avg_score",
    "early_min_score",
    "early_max_score",
    "early_assessment_count",
    "second_assessment_date",
    "score_trend",
    "gender",
    "region",
    "highest_education",
    "imd_band",
    "age_band",
    "num_of_prev_attempts",
    "studied_credits",
    "disability",
    "clicks_before_cutoff",
    "active_days_before_cutoff",
    "unique_resources_before_cutoff",
    "vle_records_before_cutoff",
    "average_daily_clicks_before_cutoff",
]


# ============================================================
# LOAD MODELS AND DATA
# ============================================================

def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}"
        )


for path in [
    PERFORMANCE_MODEL_PATH,
    RISK_MODEL_PATH,
    STUDENT_DATA_PATH,
    ML_DATA_PATH,
]:
    require_file(path)


performance_model = joblib.load(PERFORMANCE_MODEL_PATH)
risk_model = joblib.load(RISK_MODEL_PATH)

student_data = pd.read_csv(STUDENT_DATA_PATH)
ml_data = pd.read_csv(ML_DATA_PATH)


if "id_student" not in student_data.columns:
    raise ValueError(
        f"'id_student' is missing from {STUDENT_DATA_PATH}"
    )

if "id_student" not in ml_data.columns:
    raise ValueError(
        f"'id_student' is missing from {ML_DATA_PATH}"
    )


missing_features = [
    feature
    for feature in MODEL_FEATURES
    if feature not in ml_data.columns
]

if missing_features:
    logger.warning(
        "ML dataset is missing model features: %s",
        missing_features,
    )


logger.info("EduAssist models and datasets loaded successfully.")
logger.info("Student dataset rows: %s", len(student_data))
logger.info("ML dataset rows: %s", len(ml_data))


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="EduAssist AI API",
    description=(
        "AI Academic Assistant with student intelligence, "
        "RAG retrieval, and Ollama response generation."
    ),
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class PredictionRequest(BaseModel):
    code_module: str
    code_presentation: str
    first_score: float
    second_score: float
    early_avg_score: float
    early_min_score: float
    early_max_score: float
    early_assessment_count: int
    second_assessment_date: float
    score_trend: float
    gender: str
    region: str
    highest_education: str
    imd_band: str
    age_band: str
    num_of_prev_attempts: int
    studied_credits: int
    disability: str
    clicks_before_cutoff: float
    active_days_before_cutoff: float
    unique_resources_before_cutoff: float
    vle_records_before_cutoff: float
    average_daily_clicks_before_cutoff: float


class ChatRequest(BaseModel):
    student_id: int
    question: str = Field(min_length=1, max_length=2000)


# ============================================================
# DATA HELPERS
# ============================================================

def get_student_rows(student_id: int) -> pd.DataFrame:
    return student_data[
        student_data["id_student"] == student_id
    ]


def get_ml_rows(student_id: int) -> pd.DataFrame:
    return ml_data[
        ml_data["id_student"] == student_id
    ]


def clean_value(value: Any) -> Any:
    """Convert pandas/numpy values into JSON-safe values."""

    if isinstance(value, dict):
        return {
            str(key): clean_value(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            clean_value(item)
            for item in value
        ]

    if value is None:
        return None

    if hasattr(value, "item"):
        try:
            value = value.item()
        except (ValueError, TypeError):
            pass

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    return value


def build_model_input(
    source: Dict[str, Any],
) -> pd.DataFrame:

    missing = [
        feature
        for feature in MODEL_FEATURES
        if feature not in source
    ]

    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Missing model features: {missing}",
        )

    return pd.DataFrame([
        {
            feature: source[feature]
            for feature in MODEL_FEATURES
        }
    ])


# ============================================================
# MODEL PREDICTIONS
# ============================================================

def predict_future_score(student_id: int) -> Dict[str, Any]:
    rows = get_ml_rows(student_id)

    if rows.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No ML data found for student {student_id}",
        )

    row = rows.iloc[0]

    missing = [
        feature
        for feature in MODEL_FEATURES
        if feature not in rows.columns
    ]

    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"ML dataset is missing features: {missing}",
        )

    features = pd.DataFrame([
        {
            feature: row[feature]
            for feature in MODEL_FEATURES
        }
    ])

    prediction = float(
        performance_model.predict(features)[0]
    )

    return {
        "student_id": student_id,
        "predicted_future_average_score": round(
            prediction, 2
        ),
        "model": "Gradient Boosting",
    }


def predict_academic_risk(student_id: int) -> Dict[str, Any]:
    rows = get_ml_rows(student_id)

    if rows.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No ML data found for student {student_id}",
        )

    row = rows.iloc[0]

    missing = [
        feature
        for feature in MODEL_FEATURES
        if feature not in rows.columns
    ]

    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"ML dataset is missing features: {missing}",
        )

    features = pd.DataFrame([
        {
            feature: row[feature]
            for feature in MODEL_FEATURES
        }
    ])

    prediction = risk_model.predict(features)[0]

    result = {
        "student_id": student_id,
        "predicted_risk": str(prediction),
        "model": "Risk Classification",
    }

    if hasattr(risk_model, "predict_proba"):
        try:
            probabilities = risk_model.predict_proba(
                features
            )[0]

            result["risk_probabilities"] = {
                str(label): round(float(probability), 4)
                for label, probability in zip(
                    risk_model.classes_,
                    probabilities,
                )
            }

        except Exception:
            logger.exception(
                "Risk probabilities failed for student %s",
                student_id,
            )

    return result


# ============================================================
# CHAT PREDICTION RESPONSE HELPERS
# ============================================================

def generate_future_score_response(student_id: int) -> str:
    result = predict_future_score(student_id)

    return (
        "The model predicts a future average score of "
        f"{result['predicted_future_average_score']:.2f} "
        f"for student {student_id}.\n\n"
        "This is an estimate based on available data, "
        "not a guarantee of your final result."
    )


def generate_risk_response(student_id: int) -> str:
    result = predict_academic_risk(student_id)

    return (
        f"The academic risk model classifies student "
        f"{student_id} as '{result['predicted_risk']}'.\n\n"
        "Use this as an early-warning indicator alongside "
        "assessment scores and engagement trends."
    )


# ============================================================
# ROUTES
# ============================================================

@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "message": "Welcome to EduAssist AI API",
        "version": app.version,
        "docs": "/docs",
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "student_rows": int(len(student_data)),
        "ml_rows": int(len(ml_data)),
        "performance_model_loaded": performance_model is not None,
        "risk_model_loaded": risk_model is not None,
    }


@app.get("/model-status")
def model_status() -> Dict[str, Any]:
    return {
        "performance_model": PERFORMANCE_MODEL_PATH.name,
        "risk_model": RISK_MODEL_PATH.name,
        "student_dataset_rows": int(len(student_data)),
        "ml_dataset_rows": int(len(ml_data)),
        "model_features": MODEL_FEATURES,
    }


@app.post("/predict/performance")
def predict_performance(
    request: PredictionRequest,
) -> Dict[str, Any]:

    started = time.perf_counter()

    try:
        features = build_model_input(
            request.model_dump()
        )

        prediction = float(
            performance_model.predict(features)[0]
        )

        logger.info(
            "Manual performance prediction completed in %.3fs",
            time.perf_counter() - started,
        )

        return {
            "predicted_future_average_score": round(
                prediction, 2
            )
        }

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            "Manual performance prediction failed"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Performance prediction failed. "
                "Check backend logs."
            ),
        ) from exc


@app.post("/predict/risk")
def predict_risk(
    request: PredictionRequest,
) -> Dict[str, Any]:

    started = time.perf_counter()

    try:
        features = build_model_input(
            request.model_dump()
        )

        prediction = risk_model.predict(features)[0]

        result = {
            "predicted_risk": str(prediction)
        }

        if hasattr(risk_model, "predict_proba"):
            try:
                probabilities = risk_model.predict_proba(
                    features
                )[0]

                result["risk_probabilities"] = {
                    str(label): round(float(probability), 4)
                    for label, probability in zip(
                        risk_model.classes_,
                        probabilities,
                    )
                }

            except Exception:
                logger.exception(
                    "Manual risk probability calculation failed"
                )

        logger.info(
            "Manual risk prediction completed in %.3fs",
            time.perf_counter() - started,
        )

        return result

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            "Manual risk prediction failed"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Risk prediction failed. "
                "Check backend logs."
            ),
        ) from exc


@app.get("/student/{student_id}")
def get_student(student_id: int) -> Dict[str, Any]:
    rows = get_student_rows(student_id)

    if rows.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found",
        )

    return clean_value(
        rows.iloc[0].to_dict()
    )


@app.get("/student/{student_id}/intelligence")
def student_intelligence(
    student_id: int,
) -> Dict[str, Any]:

    if get_student_rows(student_id).empty:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found",
        )

    started = time.perf_counter()

    try:
        result = get_student_intelligence(student_id)

        logger.info(
            "Student intelligence completed in %.3fs",
            time.perf_counter() - started,
        )

        return clean_value(result)

    except Exception as exc:
        logger.exception(
            "Student intelligence failed for student %s",
            student_id,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not build student intelligence. "
                "Check backend logs."
            ),
        ) from exc


@app.get("/student/{student_id}/insights")
def student_insights(
    student_id: int,
) -> Dict[str, Any]:

    if get_student_rows(student_id).empty:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found",
        )

    started = time.perf_counter()

    try:
        intelligence = get_student_intelligence(
            student_id
        )

        insights = generate_academic_insights(
            intelligence
        )

        logger.info(
            "Academic insights completed in %.3fs",
            time.perf_counter() - started,
        )

        return clean_value(insights)

    except Exception as exc:
        logger.exception(
            "Academic insights failed for student %s",
            student_id,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not generate academic insights. "
                "Check backend logs."
            ),
        ) from exc


# ============================================================
# CHAT
# Fast analytics use chat.py.
# General academic questions use the existing RAG + LLM pipeline.
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest) -> Dict[str, Any]:

    request_started = time.perf_counter()

    student_id = request.student_id
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty",
        )

    if get_student_rows(student_id).empty:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} not found",
        )

    try:
        result = handle_chat(
            student_id=student_id,
            question=question,
            future_score_handler=generate_future_score_response,
            risk_handler=generate_risk_response,
        )

        logger.info(
            "POST /chat completed: student=%s intent=%s total=%.3fs",
            student_id,
            result.get("intent", "UNKNOWN"),
            time.perf_counter() - request_started,
        )

        return clean_value(result)

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception(
            "POST /chat failed for student=%s after %.3fs",
            student_id,
            time.perf_counter() - request_started,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "EduAssist AI could not complete this request. "
                "Check the backend terminal logs."
            ),
        ) from exc
