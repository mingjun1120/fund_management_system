import time
import uuid
import uvicorn
import logging
from fastapi import FastAPI, Request
from app.api.routes import router as funds_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.error_handlers import (
    DatabaseError, FundNotFoundError, ValidationError,
    database_exception_handler, fund_not_found_exception_handler,
    validation_exception_handler, http_exception_handler,
    request_validation_exception_handler, general_exception_handler
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fund_management")

# Create FastAPI app
app = FastAPI(
    title="Fund Management System API",
    description="A RESTful API for managing investment funds",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all requests and capture timing information."""
    # Generate a unique ID for this request
    request_id = str(uuid.uuid4())
    # Record start time
    start_time = time.time()
    
    # Add request ID to the request state for logging
    request.state.request_id = request_id
    
    # Log the incoming request
    logger.info(
        f"Request {request_id} started: {request.method} {request.url.path} "
        f"from {request.client.host if request.client else 'unknown'}"
    )
    
    try:
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add custom headers to the response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        
        # Log the response
        logger.info(
            f"Request {request_id} completed: Status {response.status_code} "
            f"({process_time:.4f}s)"
        )
        
        return response
    except Exception as e:
        # Log the error
        process_time = time.time() - start_time
        logger.error(
            f"Request {request_id} failed after {process_time:.4f}s: {str(e)}",
            exc_info=True
        )
        
        # Re-raise the exception to be handled by exception handlers
        raise

# Register exception handlers
app.add_exception_handler(DatabaseError, database_exception_handler)
app.add_exception_handler(FundNotFoundError, fund_not_found_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(funds_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint providing API information."""
    logger.info("Root endpoint accessed")
    
    return {
        "name": "Fund Management System API",
        "version": "1.0.0",
        "description": "A RESTful API for managing investment funds",
        "documentation": "/docs",
        "alternative_documentation": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    logger.info("Health check endpoint accessed")
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    logger.info("Starting Fund Management System API")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)