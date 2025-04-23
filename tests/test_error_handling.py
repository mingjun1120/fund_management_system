from uuid import uuid4
from app.utils.error_handlers import DatabaseError, FundNotFoundError, ValidationError

class TestErrorHandling:
    """Tests for error handling mechanisms."""
    
    def test_database_error_handler(self, client, monkeypatch):
        """Test handling of database errors."""
        # Override the get_all_funds method to raise a DatabaseError
        def mock_get_all_funds(*args, **kwargs):
            raise DatabaseError("Test database error", {"detail": "Connection failed"})
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "get_all_funds", mock_get_all_funds)
        
        # Make the request
        response = client.get("/api/funds/")
        
        # Check status code - should be server error (500)
        assert response.status_code == 500
        
        # Check response content
        data = response.json()
        assert data["error"] == "Database Error"
        assert "Test database error" in data["message"]
        assert "detail" in data["details"]
    
    def test_fund_not_found_error_handler(self, client, monkeypatch):
        """Test handling of fund not found errors."""
        # Generate a non-existent ID
        non_existent_id = str(uuid4())
        
        # Override the get_fund_by_id method to raise a FundNotFoundError
        def mock_get_fund_by_id(*args, **kwargs):
            raise FundNotFoundError(non_existent_id)
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "get_fund_by_id", mock_get_fund_by_id)
        
        # Make the request
        response = client.get(f"/api/funds/{non_existent_id}")
        
        # Check status code - should be not found (404)
        assert response.status_code == 404
        
        # Check response content
        data = response.json()
        assert data["error"] == "Not Found"
        assert non_existent_id in data["message"]
    
    def test_validation_error_handler(self, client, monkeypatch):
        """Test handling of validation errors."""
        # Override the create_fund method to raise a ValidationError
        def mock_create_fund(*args, **kwargs):
            raise ValidationError("Test validation error", [
                {"field": "name", "error": "Name cannot be empty"},
                {"field": "nav", "error": "NAV must be positive"}
            ])
        
        # Apply the monkey patch
        from app.database.db import Database
        monkeypatch.setattr(Database, "create_fund", mock_create_fund)
        
        # Prepare test data
        fund_data = {
            "name": "Test Fund",
            "manager_name": "Test Manager",
            "description": "A test fund",
            "nav": 1000.0,
            "performance": 5.0
        }
        
        # Make the request
        response = client.post("/api/funds/", json=fund_data)
        
        # Check status code - should be bad request (400)
        assert response.status_code == 400
        
        # Check response content
        data = response.json()
        assert data["error"] == "Validation Error"
        assert "Test validation error" in data["message"]
        assert "errors" in data
        assert len(data["errors"]) == 2
    
    def test_request_validation_error(self, client):
        """Test handling of request validation errors."""
        # Prepare invalid test data
        invalid_data = {
            # Missing required fields
        }
        
        # Make the request
        response = client.post("/api/funds/", json=invalid_data)
        
        # Check status code - should be unprocessable entity (422)
        assert response.status_code == 422
        
        # Check response content
        data = response.json()
        assert data["error"] == "Validation Error"
        assert "errors" in data
        assert len(data["errors"]) > 0