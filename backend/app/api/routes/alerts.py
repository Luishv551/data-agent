"""Alerts and daily KPI endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.dependencies import get_alerts_handler
from app.core.alerts_handler import AlertsHandler
from app.models.responses import AlertsResponse

router = APIRouter()


@router.get(
    "/alerts",
    response_model=AlertsResponse,
    summary="Get daily KPIs and alerts",
    description="Returns daily summary with D-1, D-7, D-30 variations and active anomaly alerts"
)
async def get_alerts(
    period: str = Query('d30', regex='^(d1|d7|d30)$', description="Period for top insights: d1, d7, or d30"),
    metric: str = Query('tpv', regex='^(tpv|average_ticket|transactions)$', description="Metric for daily summary: tpv, average_ticket, or transactions"),
    alerts_handler: AlertsHandler = Depends(get_alerts_handler)
) -> AlertsResponse:
    """Get daily KPIs and anomaly alerts.

    Args:
        period: Period for top insights calculation (d1, d7, d30)
        metric: Metric for daily summary (tpv, average_ticket, transactions)
        alerts_handler: Injected AlertsHandler instance

    Returns:
        AlertsResponse with daily summary, alerts, and top insights

    Raises:
        HTTPException: If alerts calculation fails
    """
    try:
        daily_summary = alerts_handler.get_daily_summary(metric)
        alerts = alerts_handler.detect_anomalies()
        top_insights = alerts_handler.get_top_insights(period)

        return AlertsResponse(
            daily_summary=daily_summary,
            alerts=alerts,
            top_insights=top_insights
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate alerts: {str(e)}")
