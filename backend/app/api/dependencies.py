"""Shared dependencies for API routes."""

from functools import lru_cache
from app.core.config import settings
from app.core.data_handler import DataHandler
from app.core.llm_handler import LLMHandler
from app.core.query_executor import QueryExecutor


@lru_cache()
def get_data_handler() -> DataHandler:
    """Get cached DataHandler instance.

    Returns:
        DataHandler instance with loaded data
    """
    return DataHandler(settings.DATA_PATH)


@lru_cache()
def get_llm_handler() -> LLMHandler:
    """Get cached LLMHandler instance.

    Returns:
        LLMHandler instance

    Raises:
        ValueError: If OpenAI API key is not configured
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not configured")

    return LLMHandler(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL
    )


def get_query_executor() -> QueryExecutor:
    """Get QueryExecutor instance.

    Returns:
        QueryExecutor instance with DataHandler dependency
    """
    data_handler = get_data_handler()
    return QueryExecutor(data_handler)
