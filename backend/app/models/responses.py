"""Response models."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class DataSummaryResponse(BaseModel):
    """Response model for data summary."""

    total_rows: int = Field(..., description="Total number of rows in dataset")
    date_range: Dict[str, str] = Field(..., description="Start and end dates")
    total_tpv: float = Field(..., description="Total Payment Volume")
    average_ticket: float = Field(..., description="Average ticket value")
    unique_entities: int = Field(..., description="Number of unique entities")
    unique_products: int = Field(..., description="Number of unique products")
    unique_merchants: float = Field(..., description="Total number of merchants")


class QueryIntent(BaseModel):
    """Query intent structure from LLM."""

    metric: str = Field(..., description="Metric to calculate")
    aggregation: str = Field(..., description="Aggregation function")
    group_by: List[str] = Field(default_factory=list, description="Columns to group by")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Filters to apply")
    sort_by: Optional[str] = Field(None, description="Column to sort by")
    sort_order: Optional[str] = Field("desc", description="Sort order")
    limit: Optional[int] = Field(None, description="Limit number of results")
    explanation: str = Field(..., description="Explanation of the query")


class QueryResponse(BaseModel):
    """Response model for query execution."""

    data: List[Dict[str, Any]] = Field(..., description="Result data")
    metric_value: Optional[float] = Field(None, description="Single metric value if applicable")
    metric_name: str = Field(..., description="Name of the metric")
    explanation: str = Field(..., description="Explanation of what was computed")
    query_intent: QueryIntent = Field(..., description="Original query intent from LLM")


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Response model for errors."""

    detail: str = Field(..., description="Error message")
