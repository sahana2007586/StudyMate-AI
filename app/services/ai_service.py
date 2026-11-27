import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SYSTEM_PROMPT = """You are StudyMate AI, a helpful tutor for students in India.
Adapt explanations to the learner's question and use clear, supportive language.
Explain concepts accurately, show reasoning where useful, and use examples.
Do not invent facts, syllabus details, citations, or exam predictions. If a
question depends on missing context or information you cannot verify, say so
and ask a focused follow-up question. For code, use fenced code blocks and
explain important changes. Help learners understand rather than only giving
answers."""

MODE_INSTRUCTIONS = {
    "general": "Answer the student's study question directly and clearly.",
    "explain": "Explain the topic in simple language, then give a useful example.",
    "short_notes": "Create concise, exam-revision notes using headings and bullets.",
    "detailed_notes": "Create detailed, well-organized notes with definitions, examples, and key points.",
    "summarize": "Summarize the topic accurately, separating the central ideas from supporting details.",
    "practice": "Create practice questions on the requested topic and include answers with brief explanations.",
    "quiz": "Create a short quiz with clear questions, answer options where appropriate, and an answer key with explanations.",
    "programming": "Teach the programming concept step by step and use a small, correct code example where helpful.",
    "debug": "Help debug the provided code or error. Identify likely causes, explain the fix, and ask for missing details when needed.",
}


class AIServiceError(Exception):
    """An expected configuration or provider error safe to show to the user."""

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


def generate_answer(messages, mode, api_key, base_url, model, timeout):
    """Send conversation context to an OpenAI-compatible chat completions API."""
    if not api_key:
        raise AIServiceError(
            "The AI assistant is not configured. Set STUDYMATE_AI_API_KEY in your environment and restart the app.",
            503,
        )

    api_messages = [
        {
            "role": "system",
            "content": f"{SYSTEM_PROMPT}\n\nStudy mode: {MODE_INSTRUCTIONS[mode]}",
        },
        *messages,
    ]
    request_body = json.dumps(
        {
            "model": model,
            "messages": api_messages,
        }
    ).encode("utf-8")
    provider_request = Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=request_body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(provider_request, timeout=timeout) as response:
            provider_payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:

        status_code = 503 if error.code == 429 else 502
        message = (
            "The AI provider is busy. Please try again shortly."
            if error.code == 429
            else f"The AI provider request failed (HTTP {error.code})."
        )
        error.close()
        raise AIServiceError(message, status_code) from None
    except (URLError, TimeoutError, OSError):
        raise AIServiceError(
            "Could not connect to the AI provider. Check your connection and try again.",
            502,
        ) from None
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise AIServiceError("The AI provider returned an invalid response.", 502) from None

    try:
        answer = provider_payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise AIServiceError("The AI provider returned an unexpected response.", 502) from None

    if not isinstance(answer, str) or not answer.strip():
        raise AIServiceError("The AI provider returned an empty answer.", 502)

    return answer.strip()
