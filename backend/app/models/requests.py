"""Request models."""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for natural language queries."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Natural language question about the data",
        examples=["Which product has the highest TPV?"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Which product has the highest TPV?"
            }
        }
