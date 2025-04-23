import pytest
from uuid import uuid4
from app.models.fund import Fund
from app.utils.error_handlers import FundNotFoundError#, ValidationError, DatabaseError

class TestDatabase:
    """Tests for database operations."""
    
    def test_get_all_funds(self, populated_db, sample_funds):
        """Test retrieving all funds from the database."""
        funds = populated_db.get_all_funds()
        
        # Check that we got the right number of funds
        assert len(funds) == len(sample_funds)
        
        # Check that all funds are returned
        fund_names = [fund.name for fund in funds]
        for sample_fund in sample_funds:
            assert sample_fund.name in fund_names
    
    def test_get_fund_by_id(self, populated_db, sample_funds):
        """Test retrieving a fund by ID."""
        # Get a sample fund ID
        sample_fund = sample_funds[0]
        
        # Retrieve the fund by ID
        fund = populated_db.get_fund_by_id(sample_fund.fund_id)
        
        # Check that we got the right fund
        assert fund.fund_id == sample_fund.fund_id
        assert fund.name == sample_fund.name
        assert fund.manager_name == sample_fund.manager_name
    
    def test_get_fund_by_id_not_found(self, populated_db):
        """Test retrieving a non-existent fund."""
        non_existent_id = str(uuid4())
        
        # Try to retrieve a non-existent fund
        with pytest.raises(FundNotFoundError) as excinfo:
            populated_db.get_fund_by_id(non_existent_id)
        
        # Check error message
        assert str(non_existent_id) in str(excinfo.value)
    
    def test_create_fund(self, test_db):
        """Test creating a new fund."""
        # Create a new fund
        new_fund = Fund(
            name="New Test Fund",
            manager_name="New Manager",
            description="A new test fund",
            nav=2000000.0,
            performance=7.5
        )
        
        # Save to database
        saved_fund = test_db.create_fund(new_fund)
        
        # Check that the fund was saved with the right data
        assert saved_fund.fund_id == new_fund.fund_id
        assert saved_fund.name == "New Test Fund"
        
        # Verify by retrieving from database
        retrieved_fund = test_db.get_fund_by_id(new_fund.fund_id)
        assert retrieved_fund.fund_id == new_fund.fund_id
        assert retrieved_fund.name == "New Test Fund"
    
    def test_create_fund_validation(self, test_db):
        """Test creating a fund with invalid data."""
        
        # This should raise a ValidationError
        with pytest.raises(ValueError, match="Fund name must be a non-empty string"):

            # Try to create a fund with an empty name
            invalid_fund = Fund(
                name="",  # This should trigger validation in __post_init__
                manager_name="Test Manager",
                description="Test Description",
                nav=1000.0,
                performance=5.0
            )

            test_db.create_fund(invalid_fund)
    
    def test_update_fund_performance(self, populated_db, sample_funds):
        """Test updating a fund's performance."""
        # Get a sample fund
        sample_fund = sample_funds[0]
        
        # Update the performance
        new_performance = 15.0
        updated_fund = populated_db.update_fund_performance(sample_fund.fund_id, new_performance)
        
        # Check that the performance was updated
        assert updated_fund.performance == new_performance
        
        # Verify by retrieving from database
        retrieved_fund = populated_db.get_fund_by_id(sample_fund.fund_id)
        assert retrieved_fund.performance == new_performance
    
    def test_update_fund_performance_not_found(self, populated_db):
        """Test updating a non-existent fund."""
        non_existent_id = str(uuid4())
        
        # Try to update a non-existent fund
        with pytest.raises(FundNotFoundError) as excinfo:
            populated_db.update_fund_performance(non_existent_id, 10.0)
        
        # Check error message
        assert str(non_existent_id) in str(excinfo.value)
    
    def test_delete_fund(self, populated_db, sample_funds):
        """Test deleting a fund."""
        # Get a sample fund
        sample_fund = sample_funds[0]
        
        # Delete the fund
        result = populated_db.delete_fund(sample_fund.fund_id)
        
        # Check that deletion was successful
        assert result is True
        
        # Check that the fund was deleted
        with pytest.raises(FundNotFoundError):
            populated_db.get_fund_by_id(sample_fund.fund_id)
        
        # Check that we have one less fund
        remaining_funds = populated_db.get_all_funds()
        assert len(remaining_funds) == len(sample_funds) - 1
    
    def test_delete_fund_not_found(self, populated_db):
        """Test deleting a non-existent fund."""
        non_existent_id = str(uuid4())
        
        # Try to delete a non-existent fund
        with pytest.raises(FundNotFoundError) as excinfo:
            populated_db.delete_fund(non_existent_id)
        
        # Check error message
        assert str(non_existent_id) in str(excinfo.value)