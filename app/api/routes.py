from fastapi import APIRouter, Depends, status #, HTTPException
from typing import List
import logging

from app.utils.error_handlers import DatabaseError, FundNotFoundError, ValidationError
from app.models.schemas import FundCreate, FundUpdate, FundResponse
from app.models.fund import Fund
from app.config import ACTIVE_DATABASE, DatabaseType

# Import databases
if ACTIVE_DATABASE == DatabaseType.SQLITE:
    from app.database.db import get_db
else:
    from app.database.json_db import get_json_db as get_db

# Configure logging
logger = logging.getLogger("fund_management")

# Create router instance
router = APIRouter(prefix="/api/funds", tags=["funds"])

@router.get("/", response_model=List[FundResponse])
async def get_all_funds(db = Depends(get_db)):
    """
    Retrieve a list of all investment funds.
    
    Returns:
        List[FundResponse]: A list of all funds in the system.
    
    Raises:
        DatabaseError: If there's an error accessing the database.
    """
    try:
        logger.info("Request to get all funds")
        
        funds = db.get_all_funds()
        
        logger.info(f"Retrieved {len(funds)} funds")
        return funds
    except DatabaseError:
        # Let the exception handler handle DatabaseError
        raise
    except Exception as e:
        # Log unexpected errors and convert to DatabaseError
        logger.error(f"Unexpected error in get_all_funds: {str(e)}", exc_info=True)
        raise DatabaseError("An unexpected error occurred while retrieving funds", {"error": str(e)})

@router.post("/", response_model=FundResponse, status_code=status.HTTP_201_CREATED)
async def create_fund(fund_data: FundCreate, db = Depends(get_db)):
    """
    Create a new investment fund.
    
    Args:
        fund_data (FundCreate): The data for the new fund.
        
    Returns:
        FundResponse: The created fund with all attributes.
        
    Raises:
        ValidationError: If the fund data is invalid.
        DatabaseError: If there's an error creating the fund.
    """
    try:
        logger.info(f"Request to create new fund: {fund_data.name}")
        
        # Create a new Fund instance
        new_fund = Fund(
            name=fund_data.name,
            manager_name=fund_data.manager_name,
            description=fund_data.description,
            nav=fund_data.nav,
            performance=fund_data.performance
        )
        
        # Persist to database
        created_fund = db.create_fund(new_fund)
        logger.info(f"Fund created successfully: {created_fund.fund_id}")
        return created_fund
    except ValidationError:
        # Let the exception handler handle ValidationError
        logger.warning(f"Validation error when creating fund: {fund_data.name}")
        raise
    except DatabaseError:
        # Let the exception handler handle DatabaseError
        logger.error(f"Database error when creating fund: {fund_data.name}")
        raise
    except ValueError as e:
        # Convert ValueError to ValidationError
        logger.warning(f"Value error when creating fund: {str(e)}")
        raise ValidationError("Invalid fund data", [{"error": str(e)}])
    except Exception as e:
        # Log unexpected errors and convert to DatabaseError
        logger.error(f"Unexpected error in create_fund: {str(e)}", exc_info=True)
        raise DatabaseError("An unexpected error occurred while creating the fund", {"error": str(e)})

@router.get("/{fund_id}", response_model=FundResponse)
async def get_fund(fund_id: str, db = Depends(get_db)):
    """
    Retrieve a specific fund by ID.
    
    Args:
        fund_id (str): The ID of the fund to retrieve.
        
    Returns:
        FundResponse: The requested fund.
        
    Raises:
        FundNotFoundError: If the fund doesn't exist.
        DatabaseError: If there's an error accessing the database.
    """
    try:
        logger.info(f"Request to get fund by ID: {fund_id}")
        fund = db.get_fund_by_id(fund_id)
        logger.info(f"Retrieved fund: {fund.name}")
        return fund
    except FundNotFoundError:
        # Let the exception handler handle FundNotFoundError
        logger.warning(f"Fund not found: {fund_id}")
        raise
    except DatabaseError:
        # Let the exception handler handle DatabaseError
        logger.error(f"Database error when getting fund {fund_id}")
        raise
    except Exception as e:
        # Log unexpected errors and convert to DatabaseError
        logger.error(f"Unexpected error in get_fund: {str(e)}", exc_info=True)
        raise DatabaseError(f"An unexpected error occurred while retrieving fund {fund_id}", {"error": str(e)})

@router.patch("/{fund_id}/performance", response_model=FundResponse)
async def update_fund_performance(fund_id: str, update_data: FundUpdate, db = Depends(get_db)):
    """
    Update the performance of a specific fund.
    
    Args:
        fund_id (str): The ID of the fund to update.
        update_data (FundUpdate): The new performance value.
        
    Returns:
        FundResponse: The updated fund.
        
    Raises:
        FundNotFoundError: If the fund doesn't exist.
        ValidationError: If the performance value is invalid.
        DatabaseError: If there's an error updating the fund.
    """
    try:
        logger.info(f"Request to update performance for fund {fund_id}: {update_data.performance}")
        
        # Validate performance value
        if not isinstance(update_data.performance, (int, float)):
            logger.warning(f"Invalid performance value for fund {fund_id}: {update_data.performance}")
            raise ValidationError("Invalid performance value", [
                {"field": "performance", "error": "Performance must be a number"}
            ])
        
        # Update in database
        updated_fund = db.update_fund_performance(fund_id, update_data.performance)
        logger.info(f"Updated performance for fund {fund_id} to {update_data.performance}")
        return updated_fund
    except FundNotFoundError:
        # Let the exception handler handle FundNotFoundError
        logger.warning(f"Fund not found when updating performance: {fund_id}")
        raise
    except ValidationError:
        # Let the exception handler handle ValidationError
        logger.warning(f"Validation error when updating fund performance: {fund_id}")
        raise
    except DatabaseError:
        # Let the exception handler handle DatabaseError
        logger.error(f"Database error when updating fund performance: {fund_id}")
        raise
    except Exception as e:
        # Log unexpected errors and convert to DatabaseError
        logger.error(f"Unexpected error in update_fund_performance: {str(e)}", exc_info=True)
        raise DatabaseError(f"An unexpected error occurred while updating fund {fund_id}", {"error": str(e)})
    
    # updated_fund = db.update_fund_performance(fund_id, update_data.performance)
    
    # if updated_fund is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Fund with ID {fund_id} not found"
    #     )
    
    # return updated_fund

@router.delete("/{fund_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fund(fund_id: str, db = Depends(get_db)):
    """
    Delete a fund by ID.
    
    Args:
        fund_id (str): The ID of the fund to delete.
        
    Returns:
        None
        
    Raises:
        FundNotFoundError: If the fund doesn't exist.
        DatabaseError: If there's an error deleting the fund.
    """
    try:
        logger.info(f"Request to delete fund: {fund_id}")
        
        # Delete from database
        db.delete_fund(fund_id)
        logger.info(f"Fund deleted successfully: {fund_id}")
        return None
    except FundNotFoundError:
        # Let the exception handler handle FundNotFoundError
        logger.warning(f"Fund not found when attempting to delete: {fund_id}")
        raise
    except DatabaseError:
        # Let the exception handler handle DatabaseError
        logger.error(f"Database error when deleting fund: {fund_id}")
        raise
    except Exception as e:
        # Log unexpected errors and convert to DatabaseError
        logger.error(f"Unexpected error in delete_fund: {str(e)}", exc_info=True)
        raise DatabaseError(f"An unexpected error occurred while deleting fund {fund_id}", {"error": str(e)})

    # result = db.delete_fund(fund_id)
    
    # if not result:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Fund with ID {fund_id} not found"
    #     )