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


class DailySummary(BaseModel):
    """Daily summary with variations."""

    date: str = Field(..., description="Date of the summary")
    metric: str = Field(..., description="Metric type: tpv, average_ticket, transactions")
    metric_label: str = Field(..., description="Human-readable metric label")
    value_current: float = Field(..., description="Current value for the metric")
    var_d1: float = Field(..., description="Variation vs D-1 (%)")
    var_d7: float = Field(..., description="Variation vs D-7 (%)")
    var_d30: float = Field(..., description="Variation vs D-30 (%)")


class Alert(BaseModel):
    """Anomaly alert for a specific segment."""

    type: str = Field(..., description="Alert type: warning or info")
    segment: str = Field(..., description="Segment name (product, entity, etc)")
    segment_value: str = Field(..., description="Segment value")
    metric: str = Field(..., description="Metric name (tpv, average_ticket)")
    variation: float = Field(..., description="Variation percentage")
    message: str = Field(..., description="Human-readable alert message")


class TopInsight(BaseModel):
    """Top insight for a specific period."""

    type: str = Field(..., description="Insight type: largest_drop, main_contributor, highest_growth")
    label: str = Field(..., description="Segment label (e.g., 'pix', 'credit')")
    segment_type: str = Field(..., description="Type of segment (product, payment_method, entity)")
    value: float = Field(..., description="Absolute value (TPV or Average Ticket)")
    variation: float = Field(..., description="Variation percentage")


class AlertsResponse(BaseModel):
    """Response model for alerts endpoint."""

    daily_summary: DailySummary = Field(..., description="Daily KPI summary")
    alerts: List[Alert] = Field(..., description="List of active alerts")
    top_insights: List[TopInsight] = Field(..., description="Top 3 insights for selected period")
