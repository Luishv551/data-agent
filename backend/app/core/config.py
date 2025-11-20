"""Application configuration."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "CloudWalk Data Agent"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # CORS Settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Data Settings
    DATA_PATH: Path = Path(__file__).parent.parent.parent.parent / "data" / "transactions.csv"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
