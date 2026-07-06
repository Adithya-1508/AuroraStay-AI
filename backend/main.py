from fastapi import FastAPI

from backend.api.middleware import register_middleware
from backend.api.v1 import router as api_v1_router
from backend.core.constants import PROJECT_NAME
from backend.core.lifecycle import lifespan
from backend.exceptions import register_exception_handlers
from backend.health import router as health_router


def create_app() -> FastAPI:
    """Assembles and configures the FastAPI application instance."""
    app = FastAPI(
        title=PROJECT_NAME,
        description=(
            "Enterprise-grade AI-powered Hospitality Platform Backend Core Framework"
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    # Register middleware pipeline
    register_middleware(app)

    # Register exception mapping rules
    register_exception_handlers(app)

    # Register API endpoints
    app.include_router(api_v1_router, prefix="/api/v1")
    app.include_router(health_router)

    return app


app = create_app()

__all__ = ["app"]
