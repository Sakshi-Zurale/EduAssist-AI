import logging
import time
from typing import Optional

import requests


# =========================================================
# OLLAMA SETTINGS
# =========================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"
REQUEST_TIMEOUT = 120

# Keep the model loaded between requests to reduce
# delays caused by unloading and reloading it.
KEEP_ALIVE = "10m"

# Limit unnecessary generation for faster responses.
GENERATION_OPTIONS = {
    "temperature": 0.2,
    "num_predict": 220,
    "num_ctx": 4096,
}

logger = logging.getLogger("eduassist.llm")


# =========================================================
# GENERATE RESPONSE
# =========================================================

def generate_response(
    prompt: str,
    system_prompt: Optional[str] = None,
) -> str:
    """Generate a response using the local Ollama model."""

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "keep_alive": KEEP_ALIVE,
        "options": GENERATION_OPTIONS,
    }

    if system_prompt:
        payload["system"] = system_prompt

    started = time.perf_counter()

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()
        result = response.json()

        answer = result.get("response", "").strip()

        elapsed = time.perf_counter() - started

        logger.info(
            "Ollama request completed: model=%s duration=%.2fs "
            "prompt_tokens=%s generated_tokens=%s",
            MODEL_NAME,
            elapsed,
            result.get("prompt_eval_count", "unknown"),
            result.get("eval_count", "unknown"),
        )

        if not answer:
            logger.warning("Ollama returned an empty response.")

        return answer

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure Ollama is running."
        ) from error

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "Ollama request timed out."
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Ollama request failed: {error}"
        ) from error

    except (ValueError, TypeError) as error:
        raise RuntimeError(
            f"Could not parse Ollama's response: {error}"
        ) from error


# =========================================================
# MANUAL TEST
# =========================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    system_prompt = """
You are EduAssist AI, a helpful academic assistant.

Explain concepts clearly and accurately.
Use simple language and short examples where useful.
Use supplied knowledge-base context when relevant.
Do not invent facts or claim to have used unavailable information.
"""

    test_questions = [
        "What is machine learning?",
        "What is cloud computing?",
        "Explain normalization in DBMS with a simple example.",
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")

        try:
            answer = generate_response(
                prompt=question,
                system_prompt=system_prompt,
            )
            print(f"EduAssist AI: {answer}")

        except (RuntimeError, ValueError) as error:
            print(f"Error: {error}")
