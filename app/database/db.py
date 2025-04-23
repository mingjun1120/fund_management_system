import os
import sqlite3
import logging
from datetime import datetime
from app.models.fund import Fund
from typing import List, Optional
from app.utils.error_handlers import DatabaseError, FundNotFoundError, ValidationError

# Configure logging
logger = logging.getLogger("fund_management")

DATABASE_PATH = os.path.join("app", "database", "funds.db")

class Database:
    """Database handler for fund management system."""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize database connection."""
        self.db_path = db_path
        try:
            # Open the connection once and store it
            self.conn = sqlite3.connect(db_path)
            
            # Enable foreign keys
            self.conn.execute("PRAGMA foreign_keys = ON")
            
            self._create_tables_if_not_exists()
        except sqlite3.Error as e:
            raise DatabaseError("Failed to initialize database", {"sqlite_error": str(e)})
    
    def _create_tables_if_not_exists(self):
        """Create database tables if they don't exist."""
        try:
            cursor = self.conn.cursor()
                
            # Create funds table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS funds (
                    fund_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    manager_name TEXT NOT NULL,
                    description TEXT,
                    nav REAL NOT NULL,
                    creation_date TEXT NOT NULL,
                    performance REAL NOT NULL
                )
            ''')
                
            self.conn.commit()
            logger.info("Database tables initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise DatabaseError("Failed to create database tables", {"sqlite_error": str(e)})
    
    def get_all_funds(self) -> List[Fund]:
        """
        Retrieve all funds from the database.
        
        Returns:
            List[Fund]: A list of all funds in the database.
            
        Raises:
            DatabaseError: If there's an error accessing the database.
        """
        try:
            # Use the existing connection instead of creating a new one
            
            # Enable row factory to get dictionary-like results
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            
            cursor.execute('SELECT * FROM funds')
            rows = cursor.fetchall()
            
            # Convert rows to Fund objects
            funds = []
            for row in rows:
                row_dict = dict(row)
                # Convert string date back to datetime
                row_dict['creation_date'] = datetime.fromisoformat(row_dict['creation_date'])
                funds.append(Fund(**row_dict))
            
            return funds
        except sqlite3.Error as e:
            logger.error(f"Database error when fetching all funds: {str(e)}")
            raise DatabaseError("Failed to retrieve funds", {"sqlite_error": str(e)})
        except ValueError as e:
            logger.error(f"Value error when parsing fund data: {str(e)}")
            raise ValidationError("Invalid fund data in database", [{"error": str(e)}])
        except Exception as e:
            logger.error(f"Unexpected error in get_all_funds: {str(e)}", exc_info=True)
            raise DatabaseError("An unexpected error occurred", {"error": str(e)})
    
    def get_fund_by_id(self, fund_id: str) -> Optional[Fund]:
        """
        Retrieve a fund by its ID.
        
        Args:
            fund_id (str): The ID of the fund to retrieve.
            
        Returns:
            Fund: The requested fund.
            
        Raises:
            FundNotFoundError: If the fund doesn't exist.
            DatabaseError: If there's an error accessing the database.
        """
        try:
    
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            
            cursor.execute('SELECT * FROM funds WHERE fund_id = ?', (fund_id,))
            row = cursor.fetchone()
            
            if row is None:
                logger.warning(f"Fund not found: {fund_id}")
                raise FundNotFoundError(fund_id)
            
            # Convert row to Fund object
            row_dict = dict(row)
            row_dict['creation_date'] = datetime.fromisoformat(row_dict['creation_date'])
            
            return Fund(**row_dict)
        except sqlite3.Error as e:
            logger.error(f"Database error when fetching fund {fund_id}: {str(e)}")
            raise DatabaseError(f"Failed to retrieve fund {fund_id}", {"sqlite_error": str(e)})
        except ValueError as e:
            logger.error(f"Value error when parsing fund data: {str(e)}")
            raise ValidationError("Invalid fund data in database", [{"error": str(e)}])
        except FundNotFoundError:
            # Re-raise FundNotFoundError exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_fund_by_id: {str(e)}", exc_info=True)
            raise DatabaseError("An unexpected error occurred", {"error": str(e)})
    
    def create_fund(self, fund: Fund) -> Fund:
        """
        Create a new fund in the database.
        
        Args:
            fund (Fund): The fund object to create.
            
        Returns:
            Fund: The created fund.
            
        Raises:
            DatabaseError: If there's an error inserting the fund.
            ValidationError: If the fund data is invalid.
        """
        try:
            cursor = self.conn.cursor()
            
            # Validate fund data
            if not fund.name:
                raise ValidationError("Fund validation failed", [{"field": "name", "error": "Name cannot be empty"}])
            
            if not fund.manager_name:
                raise ValidationError("Fund validation failed", [{"field": "manager_name", "error": "Manager name cannot be empty"}])
            
            if fund.nav < 0:
                raise ValidationError("Fund validation failed", [{"field": "nav", "error": "NAV cannot be negative"}])
            
            cursor.execute('''
                INSERT INTO funds (fund_id, name, manager_name, description, nav, creation_date, performance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                fund.fund_id,
                fund.name,
                fund.manager_name,
                fund.description,
                fund.nav,
                fund.creation_date.isoformat(),
                fund.performance
            ))
            
            self.conn.commit()
            logger.info(f"Created fund: {fund.name} (ID: {fund.fund_id})")
            
            return fund
        except sqlite3.IntegrityError as e:
            logger.error(f"Integrity error when creating fund: {str(e)}")
            if "UNIQUE constraint failed: funds.name" in str(e):
                raise ValidationError("Fund validation failed", [{"field": "name", "error": "A fund with this name already exists"}])
            else:
                raise DatabaseError("Failed to create fund due to integrity constraint", {"sqlite_error": str(e)})
        except sqlite3.Error as e:
            logger.error(f"Database error when creating fund: {str(e)}")
            raise DatabaseError("Failed to create fund", {"sqlite_error": str(e)})
        except ValidationError:
            # Re-raise ValidationError exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error in create_fund: {str(e)}", exc_info=True)
            raise DatabaseError("An unexpected error occurred", {"error": str(e)})
    
    def update_fund_performance(self, fund_id: str, performance: float) -> Optional[Fund]:
        """
        Update a fund's performance.
        
        Args:
            fund_id (str): The ID of the fund to update.
            performance (float): The new performance value.
            
        Returns:
            Fund: The updated fund.
            
        Raises:
            FundNotFoundError: If the fund doesn't exist.
            DatabaseError: If there's an error updating the fund.
            ValidationError: If the performance value is invalid.
        """
        try:
            # Validate performance value
            if not isinstance(performance, (int, float)):
                raise ValidationError("Invalid performance value", [
                    {"field": "performance", "error": "Performance must be a number"}
                ])
            
            cursor = self.conn.cursor()
            
            cursor.execute('UPDATE funds SET performance = ? WHERE fund_id = ?', (performance, fund_id))
            
            if cursor.rowcount == 0:
                # No rows affected, fund not found
                raise FundNotFoundError(fund_id) # return None
            
            self.conn.commit()
            logger.info(f"Updated performance for fund ID {fund_id} to {performance}")
            
            # Get the updated fund
            return self.get_fund_by_id(fund_id)
        except sqlite3.Error as e:
            logger.error(f"Database error when updating fund {fund_id}: {str(e)}")
            raise DatabaseError(f"Failed to update fund {fund_id}", {"sqlite_error": str(e)})
        except (FundNotFoundError, ValidationError):
            # Re-raise these specific exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error in update_fund_performance: {str(e)}", exc_info=True)
            raise DatabaseError("An unexpected error occurred", {"error": str(e)})
    
    def delete_fund(self, fund_id: str) -> bool:
        """
        Delete a fund by its ID.
        
        Args:
            fund_id (str): The ID of the fund to delete.
            
        Returns:
            bool: True if the fund was deleted, False otherwise.
            
        Raises:
            FundNotFoundError: If the fund doesn't exist.
            DatabaseError: If there's an error deleting the fund.
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('DELETE FROM funds WHERE fund_id = ?', (fund_id,))
            
            if cursor.rowcount == 0:
                # No rows affected, fund not found
                raise FundNotFoundError(fund_id) # return False
            
            self.conn.commit()
            logger.info(f"Deleted fund ID {fund_id}")
            
            return True
        except sqlite3.Error as e:
            logger.error(f"Database error when deleting fund {fund_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete fund {fund_id}", {"sqlite_error": str(e)})
        except FundNotFoundError:
            # Re-raise FundNotFoundError exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error in delete_fund: {str(e)}", exc_info=True)
            raise DatabaseError("An unexpected error occurred", {"error": str(e)})

    def close(self):
        """Close the database connection."""
        if hasattr(self, 'conn'):
            self.conn.close()
            logger.info(f"Database connection closed for {self.db_path}")

# Create a database instance
db = Database()

def get_db() -> Database:
    """Get the database instance."""
    return db