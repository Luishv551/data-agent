"""Query processing endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_llm_handler, get_query_executor
from app.core.llm_handler import LLMHandler
from app.core.query_executor import QueryExecutor
from app.models.requests import QueryRequest
from app.models.responses import QueryResponse, QueryIntent

router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Process natural language query",
    description="Converts a natural language question into a query and executes it against the dataset"
)
async def process_query(
    request: QueryRequest,
    llm_handler: LLMHandler = Depends(get_llm_handler),
    query_executor: QueryExecutor = Depends(get_query_executor)
) -> QueryResponse:
    """Process a natural language query.

    Args:
        request: QueryRequest with the user's question
        llm_handler: Injected LLMHandler instance
        query_executor: Injected QueryExecutor instance

    Returns:
        QueryResponse with results and explanation

    Raises:
        HTTPException: If query processing fails
    """
    try:
        query_intent = llm_handler.parse_question(request.question)

        result = query_executor.execute(query_intent)

        return QueryResponse(
            data=result.data.to_dict(orient='records'),
            metric_value=result.metric_value,
            metric_name=result.metric_name,
            explanation=result.explanation,
            query_intent=QueryIntent(**result.query_intent)
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")
