from uuid import uuid4
from app.models.fund import Fund

class TestAPI:
    """Tests for API endpoints."""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        
        # Check status code
        assert response.status_code == 200
        
        # Check response content
        data = response.json()
        assert "name" in data
        assert "documentation" in data
    
    def test_get_all_funds_empty(self, client, monkeypatch):
        """Test getting all funds when there are none."""
        # Override the get_all_funds method to return an empty list
        def mock_get_all_funds(*args, **kwargs):
            return []
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "get_all_funds", mock_get_all_funds)
        
        # Make the request
        response = client.get("/api/funds/")
        
        # Check status code
        assert response.status_code == 200
        
        # Check response content
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_all_funds(self, client, sample_funds, monkeypatch):
        """Test getting all funds."""
        # Override the get_all_funds method to return sample funds
        def mock_get_all_funds(*args, **kwargs):
            return sample_funds
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "get_all_funds", mock_get_all_funds)
        
        # Make the request
        response = client.get("/api/funds/")
        
        # Check status code
        assert response.status_code == 200
        
        # Check response content
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(sample_funds)
        
        # Check that all funds are returned
        fund_names = [fund["name"] for fund in data]
        for sample_fund in sample_funds:
            assert sample_fund.name in fund_names
    
    def test_create_fund(self, client, monkeypatch):
        """Test creating a new fund."""
        # Override the create_fund method to return the input
        def mock_create_fund(self, fund):
            return fund
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "create_fund", mock_create_fund)
        
        # Prepare test data
        fund_data = {
            "name": "API Test Fund",
            "manager_name": "API Test Manager",
            "description": "A fund created through the API",
            "nav": 3000000.0,
            "performance": 9.5
        }
        
        # Make the request
        response = client.post("/api/funds/", json=fund_data)
        
        # Check status code
        assert response.status_code == 201
        
        # Check response content
        data = response.json()
        assert data["name"] == fund_data["name"]
        assert data["manager_name"] == fund_data["manager_name"]
        assert data["description"] == fund_data["description"]
        assert data["nav"] == fund_data["nav"]
        assert data["performance"] == fund_data["performance"]
        assert "fund_id" in data
        assert "creation_date" in data
    
    def test_create_fund_invalid(self, client):
        """Test creating a fund with invalid data."""
        # Prepare invalid test data (missing required fields)
        invalid_data = {
            "name": "Invalid Fund",
            # Missing manager_name and other required fields
        }
        
        # Make the request
        response = client.post("/api/funds/", json=invalid_data)
        
        # Check status code - should be a validation error (422)
        assert response.status_code == 422
        
        # Check that the response indicates what's wrong
        data = response.json()
        assert "error" in data
        assert "manager_name" in str(data)  # Field name should be in the error message
    
    def test_get_fund_by_id(self, client, sample_funds, monkeypatch):
        """Test getting a fund by ID."""
        # Get a sample fund
        sample_fund = sample_funds[0]
        
        # Override the get_fund_by_id method to return the sample fund
        def mock_get_fund_by_id(self, fund_id):
            if fund_id == sample_fund.fund_id:
                return sample_fund
            from app.utils.error_handlers import FundNotFoundError
            raise FundNotFoundError(fund_id)
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "get_fund_by_id", mock_get_fund_by_id)
        
        # Make the request
        response = client.get(f"/api/funds/{sample_fund.fund_id}")
        
        # Check status code
        assert response.status_code == 200
        
        # Check response content
        data = response.json()
        assert data["fund_id"] == sample_fund.fund_id
        assert data["name"] == sample_fund.name
        assert data["manager_name"] == sample_fund.manager_name
    
    def test_get_fund_by_id_not_found(self, client, monkeypatch):
        """Test getting a non-existent fund."""
        # Generate a non-existent ID
        non_existent_id = str(uuid4())
        
        # Override the get_fund_by_id method to raise FundNotFoundError
        def mock_get_fund_by_id(self, fund_id):
            from app.utils.error_handlers import FundNotFoundError
            raise FundNotFoundError(fund_id)
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "get_fund_by_id", mock_get_fund_by_id)
        
        # Make the request
        response = client.get(f"/api/funds/{non_existent_id}")
        
        # Check status code - should be not found (404)
        assert response.status_code == 404
        
        # Check response content
        data = response.json()
        assert "error" in data
        assert str(non_existent_id) in str(data["message"])
    
    def test_update_fund_performance(self, client, sample_funds, monkeypatch):
        """Test updating a fund's performance."""
        # Get a sample fund
        sample_fund = sample_funds[0]
        
        # Create a modified version of the fund with updated performance
        updated_fund = Fund(
            fund_id=sample_fund.fund_id,
            name=sample_fund.name,
            manager_name=sample_fund.manager_name,
            description=sample_fund.description,
            nav=sample_fund.nav,
            creation_date=sample_fund.creation_date,
            performance=20.0  # New performance value
        )
        
        # Override the update_fund_performance method to return the updated fund
        def mock_update_fund_performance(self, fund_id, performance):
            if fund_id == sample_fund.fund_id:
                return updated_fund
            from app.utils.error_handlers import FundNotFoundError
            raise FundNotFoundError(fund_id)
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "update_fund_performance", mock_update_fund_performance)
        
        # Prepare update data
        update_data = {
            "performance": 20.0
        }
        
        # Make the request
        response = client.patch(f"/api/funds/{sample_fund.fund_id}/performance", json=update_data)
        
        # Check status code
        assert response.status_code == 200
        
        # Check response content
        data = response.json()
        assert data["fund_id"] == sample_fund.fund_id
        assert data["performance"] == 20.0  # Updated value
    
    def test_update_fund_performance_not_found(self, client, monkeypatch):
        """Test updating a non-existent fund."""
        # Generate a non-existent ID
        non_existent_id = str(uuid4())
        
        # Override the update_fund_performance method to raise FundNotFoundError
        def mock_update_fund_performance(self, fund_id, performance):
            from app.utils.error_handlers import FundNotFoundError
            raise FundNotFoundError(fund_id)
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "update_fund_performance", mock_update_fund_performance)
        
        # Prepare update data
        update_data = {
            "performance": 15.0
        }
        
        # Make the request
        response = client.patch(f"/api/funds/{non_existent_id}/performance", json=update_data)
        
        # Check status code - should be not found (404)
        assert response.status_code == 404
        
        # Check response content
        data = response.json()
        assert "error" in data
        assert str(non_existent_id) in str(data["message"])
    
    def test_delete_fund(self, client, sample_funds, monkeypatch):
        """Test deleting a fund."""
        # Get a sample fund
        sample_fund = sample_funds[0]
        
        # Override the delete_fund method to return True
        def mock_delete_fund(self, fund_id):
            if fund_id == sample_fund.fund_id:
                return True
            from app.utils.error_handlers import FundNotFoundError
            raise FundNotFoundError(fund_id)
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "delete_fund", mock_delete_fund)
        
        # Make the request
        response = client.delete(f"/api/funds/{sample_fund.fund_id}")
        
        # Check status code - should be no content (204)
        assert response.status_code == 204
        
        # Check response content - should be empty
        assert response.content == b''
    
    def test_delete_fund_not_found(self, client, monkeypatch):
        """Test deleting a non-existent fund."""
        # Generate a non-existent ID
        non_existent_id = str(uuid4())
        
        # Override the delete_fund method to raise FundNotFoundError
        def mock_delete_fund(self, fund_id):
            from app.utils.error_handlers import FundNotFoundError
            raise FundNotFoundError(fund_id)
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "delete_fund", mock_delete_fund)
        
        # Make the request
        response = client.delete(f"/api/funds/{non_existent_id}")
        
        # Check status code - should be not found (404)
        assert response.status_code == 404
        
        # Check response content
        data = response.json()
        assert "error" in data
        assert str(non_existent_id) in str(data["message"])