"""Data summary endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_data_handler
from app.core.data_handler import DataHandler
from app.models.responses import DataSummaryResponse

router = APIRouter()


@router.get(
    "/summary",
    response_model=DataSummaryResponse,
    summary="Get dataset summary",
    description="Returns summary statistics about the transactions dataset"
)
async def get_data_summary(
    data_handler: DataHandler = Depends(get_data_handler)
) -> DataSummaryResponse:
    """Get summary statistics about the dataset.

    Args:
        data_handler: Injected DataHandler instance

    Returns:
        DataSummaryResponse with statistics

    Raises:
        HTTPException: If data cannot be loaded
    """
    try:
        summary = data_handler.get_data_summary()
        return DataSummaryResponse(**summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get data summary: {str(e)}")
