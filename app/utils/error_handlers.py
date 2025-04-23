from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Dict, Any, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_errors.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fund_management")

# Custom exception classes
class DatabaseError(Exception):
    """Exception raised for database-related errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class FundNotFoundError(Exception):
    """Exception raised when a requested fund is not found."""
    def __init__(self, fund_id: str):
        self.fund_id = fund_id
        self.message = f"Fund with ID {fund_id} not found"
        super().__init__(self.message)


class ValidationError(Exception):
    """Exception raised for custom validation errors."""
    def __init__(self, message: str, errors: List[Dict[str, Any]]):
        self.message = message
        self.errors = errors
        super().__init__(self.message)


# Exception handlers
async def database_exception_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """Handle database-related exceptions."""
    logger.error(f"Database error: {exc.message}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database Error",
            "message": exc.message,
            "details": exc.details if exc.details else None
        }
    )


async def fund_not_found_exception_handler(request: Request, exc: FundNotFoundError) -> JSONResponse:
    """Handle fund not found exceptions."""
    logger.warning(f"Fund not found: {exc.fund_id}")
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": exc.message
        }
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle custom validation exceptions."""
    logger.warning(f"Validation error: {exc.message}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation Error",
            "message": exc.message,
            "errors": exc.errors
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions."""
    logger.warning(f"HTTP exception: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request Error",
            "message": exc.detail
        }
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation exceptions from Pydantic models."""
    errors = []
    for error in exc.errors():
        error_detail = {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        }
        errors.append(error_detail)
    
    logger.warning(f"Request validation error: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "errors": errors
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle any unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )