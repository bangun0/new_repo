"""
Main application module for the TodayPickup API Wrapper.

This module initializes the FastAPI application, sets up lifespan management for
resources (like HTTP clients via services), and includes the API routers
for different functionalities (Agency and Mall operations).
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request 

# Import services to manage their lifecycle
from app.services.agency_service import AgencyService
from app.services.mall_service import MallService

# Import routers from the controllers module
from app.controllers import agency_controller, mall_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for application lifespan events.

    This function handles:
    - **Startup**: Initializes `AgencyService` and `MallService` instances.
      These services, in turn, initialize their respective repositories,
      which set up `httpx.AsyncClient` instances. The service instances
      are stored in `app.state` to be accessible via `Request` objects
      in dependency functions (e.g., `get_agency_service`).
    - **Shutdown**: Gracefully closes the HTTP clients within the services
      by calling their `close_repository()` methods. This ensures that
      resources are properly released when the application terminates.
    """
    # Startup: Initialize services
    print("Application startup: Initializing services...")
    agency_service = AgencyService()
    mall_service = MallService()
    
    # Store service instances in app.state for access by dependency injection
    app.state.agency_service = agency_service
    app.state.mall_service = mall_service
    print("Application startup: Services initialized and stored in app.state.")
    
    yield  # The application runs while in this yielded state
    
    # Shutdown: Close repository HTTP clients managed by services
    print("Application shutdown: Closing service resources...")
    if hasattr(app.state, 'agency_service') and app.state.agency_service:
        await app.state.agency_service.close_repository()
        print("Agency service's HTTP client closed.")
    if hasattr(app.state, 'mall_service') and app.state.mall_service:
        await app.state.mall_service.close_repository()
        print("Mall service's HTTP client closed.")
    print("Application shutdown: Completed.")

# Initialize the FastAPI application.
# The title, description, and version are used for the API documentation.
# The lifespan context manager handles startup and shutdown events.
app = FastAPI(
    title="TodayPickup API Wrapper",
    description="A FastAPI application to wrap the Kakao T TodayPickup API. "
                "Provides structured endpoints for both MALL and AGENCY Open API operations.",
    version="0.1.0",
    lifespan=lifespan # Register the lifespan context manager
)

@app.get("/")
async def read_root():
    """
    Root endpoint for the API.
    Provides a welcome message and a link to the API documentation.
    """
    return {"message": "Welcome to the TodayPickup API Wrapper. See /docs for API documentation."}

# Include API routers from controller modules.
# A common prefix "/api" is used for all routes defined in these controllers.
# This helps in versioning or grouping the API under a common namespace.
app.include_router(agency_controller.router, prefix="/api") 
app.include_router(mall_controller.router, prefix="/api")
