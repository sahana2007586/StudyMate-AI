import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)


class Config:
    """Application configuration loaded from environment variables."""

    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    TESTING = os.getenv("FLASK_TESTING", "0") == "1"
    MAX_CONTENT_LENGTH = 128 * 1024
    AI_API_KEY = os.getenv("STUDYMATE_AI_API_KEY")
    AI_BASE_URL = os.getenv("STUDYMATE_AI_BASE_URL", "https://api.openai.com/v1")
    AI_MODEL = os.getenv("STUDYMATE_AI_MODEL", "gpt-4o-mini")
    AI_TIMEOUT_SECONDS = 45
