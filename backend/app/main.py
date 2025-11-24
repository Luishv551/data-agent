"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import query, data, alerts
from app.models.responses import HealthResponse

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Natural language interface for CloudWalk transaction data analysis",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix=f"{settings.API_V1_PREFIX}", tags=["Query"])
app.include_router(data.router, prefix=f"{settings.API_V1_PREFIX}/data", tags=["Data"])
app.include_router(alerts.router, prefix=f"{settings.API_V1_PREFIX}", tags=["Alerts"])


@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """Root endpoint - health check."""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.VERSION
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
