"""Response models."""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class DataSummaryResponse(BaseModel):
    """Response model for data summary."""

    total_tpv: float = Field(..., description="Total Payment Volume")
    average_ticket: float = Field(..., description="Average ticket value")


class DashboardResponse(BaseModel):
    """Response model for dashboard visualizations."""

    tpv_by_product: List[Dict[str, Any]] = Field(..., description="TPV grouped by product")
    tpv_by_entity: List[Dict[str, Any]] = Field(..., description="TPV grouped by entity")
    tpv_by_payment_method: List[Dict[str, Any]] = Field(..., description="TPV grouped by payment method")
    avg_ticket_by_entity: List[Dict[str, Any]] = Field(..., description="Average ticket by entity")
    avg_ticket_by_product: List[Dict[str, Any]] = Field(..., description="Average ticket by product")
    avg_ticket_by_payment_method: List[Dict[str, Any]] = Field(..., description="Average ticket by payment method")
    tpv_by_price_tier: List[Dict[str, Any]] = Field(..., description="TPV by price tier")
    tpv_by_installments: List[Dict[str, Any]] = Field(..., description="TPV by installments")


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
