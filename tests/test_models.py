import pytest
from datetime import datetime
from app.models.fund import Fund

class TestFundModel:
    """Tests for the Fund model."""
    
    def test_fund_creation(self):
        """Test creating a Fund object with valid data."""
        fund = Fund(
            name="Test Fund",
            manager_name="Test Manager",
            description="Test Description",
            nav=1000.0,
            performance=5.0
        )
        
        # Check that all fields are set correctly
        assert fund.name == "Test Fund"
        assert fund.manager_name == "Test Manager"
        assert fund.description == "Test Description"
        assert fund.nav == 1000.0
        assert fund.performance == 5.0
        
        # Check that auto-generated fields exist
        assert fund.fund_id is not None
        assert isinstance(fund.creation_date, datetime)
    
    def test_fund_validation(self):
        """Test Fund validation for invalid data."""
        # Test with empty name
        with pytest.raises(ValueError):
            Fund(
                name="",
                manager_name="Test Manager",
                description="Test Description",
                nav=1000.0,
                performance=5.0
            )
        
        # Test with empty manager name
        with pytest.raises(ValueError):
            Fund(
                name="Test Fund",
                manager_name="",
                description="Test Description",
                nav=1000.0,
                performance=5.0
            )
        
        # Test with negative NAV
        with pytest.raises(ValueError):
            Fund(
                name="Test Fund",
                manager_name="Test Manager",
                description="Test Description",
                nav=-1000.0,
                performance=5.0
            )
    
    def test_to_dict(self):
        """Test converting a Fund to a dictionary."""
        fund = Fund(
            name="Test Fund",
            manager_name="Test Manager",
            description="Test Description",
            nav=1000.0,
            performance=5.0
        )
        
        fund_dict = fund.to_dict()
        
        # Check all fields are in the dictionary
        assert fund_dict["fund_id"] == fund.fund_id
        assert fund_dict["name"] == "Test Fund"
        assert fund_dict["manager_name"] == "Test Manager"
        assert fund_dict["description"] == "Test Description"
        assert fund_dict["nav"] == 1000.0
        assert fund_dict["performance"] == 5.0
        assert "creation_date" in fund_dict
    
    def test_from_dict(self):
        """Test creating a Fund from a dictionary."""
        fund_dict = {
            "fund_id": "test-id-123",
            "name": "Test Fund",
            "manager_name": "Test Manager",
            "description": "Test Description",
            "nav": 1000.0,
            "creation_date": "2023-01-01T00:00:00",
            "performance": 5.0
        }
        
        fund = Fund.from_dict(fund_dict)
        
        # Check all fields are set correctly
        assert fund.fund_id == "test-id-123"
        assert fund.name == "Test Fund"
        assert fund.manager_name == "Test Manager"
        assert fund.description == "Test Description"
        assert fund.nav == 1000.0
        assert fund.performance == 5.0
        assert isinstance(fund.creation_date, datetime)