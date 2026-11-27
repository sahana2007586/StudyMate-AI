from flask import Blueprint, current_app, jsonify, render_template, request

from app.services.ai_service import AIServiceError, generate_answer


assistant = Blueprint("assistant", __name__)

MAX_MESSAGES = 16
MAX_MESSAGE_LENGTH = 6000
MAX_CONTEXT_LENGTH = 24000
STUDY_MODES = {
    "general",
    "explain",
    "short_notes",
    "detailed_notes",
    "summarize",
    "practice",
    "quiz",
    "programming",
    "debug",
}


@assistant.get("/assistant")
def page():
    """Render the AI study assistant."""
    return render_template("assistant.html")


@assistant.post("/api/chat")
def chat():
    """Validate a conversation and return a provider-generated study answer."""
    if not request.is_json:
        return jsonify(error="Send the chat request as JSON."), 415

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="The request must contain a JSON object."), 400

    mode = data.get("mode", "general")
    if not isinstance(mode, str) or mode not in STUDY_MODES:
        return jsonify(error="Choose a valid study mode."), 400

    messages = data.get("messages")
    validation_error = _validate_messages(messages)
    if validation_error:
        return jsonify(error=validation_error), 400

    try:
        answer = generate_answer(
            messages=messages,
            mode=mode,
            api_key=current_app.config.get("AI_API_KEY"),
            base_url=current_app.config["AI_BASE_URL"],
            model=current_app.config["AI_MODEL"],
            timeout=current_app.config["AI_TIMEOUT_SECONDS"],
        )
    except AIServiceError as error:
        return jsonify(error=str(error)), error.status_code

    return jsonify(answer=answer)


@assistant.errorhandler(413)
def request_too_large(_error):
    return jsonify(error="The chat request is too large. Shorten the conversation and try again."), 413


def _validate_messages(messages):
    if not isinstance(messages, list) or not messages:
        return "Add a question before sending."
    if len(messages) > MAX_MESSAGES:
        return "This conversation is too long. Clear the chat and start a new one."

    total_length = 0
    for message in messages:
        if not isinstance(message, dict):
            return "Conversation messages must have a user or assistant role."

        role = message.get("role")
        if not isinstance(role, str) or role not in {"user", "assistant"}:
            return "Conversation messages must have a user or assistant role."

        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            return "Conversation messages cannot be empty."
        if len(content) > MAX_MESSAGE_LENGTH:
            return "Each message must be 6,000 characters or fewer."
        total_length += len(content)

    if total_length > MAX_CONTEXT_LENGTH:
        return "The conversation context is too long. Clear the chat and try again."
    if messages[-1]["role"] != "user":
        return "The latest conversation message must be your question."

    return None
