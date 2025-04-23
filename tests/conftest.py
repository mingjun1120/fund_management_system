import pytest
from uuid import uuid4
from fastapi.testclient import TestClient

from main import app
from app.models.fund import Fund
from app.database.db import Database

# Test client for API testing
@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)

# Test database fixture
@pytest.fixture
def test_db():
    """Create a test database and ensure connection is closed."""
    
    # Use an in-memory SQLite database for tests
    db_path = ":memory:"
    
    # Create a test database instance (__init__ now creates connection and tables)
    db = Database(db_path) 
    
    # Return the database for testing
    yield db
    
    # Clean up: close the connection after the test using the fixture is done
    db.close()

# Sample test funds
@pytest.fixture
def sample_funds():
    """Create sample funds for testing."""
    funds = [
        Fund(
            fund_id=str(uuid4()),
            name="Test Growth Fund",
            manager_name="Jane Smith",
            description="A test growth fund for high returns",
            nav=1000000.0,
            performance=12.5
        ),
        Fund(
            fund_id=str(uuid4()),
            name="Test Income Fund",
            manager_name="John Doe",
            description="A test income fund for stable returns",
            nav=5000000.0,
            performance=5.8
        ),
        Fund(
            fund_id=str(uuid4()),
            name="Test Balanced Fund",
            manager_name="Alice Johnson",
            description="A test balanced fund with moderate risk",
            nav=3000000.0,
            performance=8.2
        )
    ]
    return funds

# Fixture to create a database with sample data
@pytest.fixture
def populated_db(test_db, sample_funds):
    """Create a test database populated with sample funds."""
    # Add the sample funds to the database
    for fund in sample_funds:
        test_db.create_fund(fund)
    
    return test_db