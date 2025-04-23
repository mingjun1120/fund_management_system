# Fund Management System
A RESTful API for managing investment funds, built with FastAPI and SQLite.

## Features
- CRUD operations for investment funds
- Performance tracking
- Comprehensive error handling
- Thorough test coverage
- API documentation

## Requirements
- Python 3.10+
- Dependencies listed in `requirements.txt` file.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/mingjun1120/fund-management-system.git
    cd fund-management-system
    ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
Start the server:
```bash
python main.py
```
The API will be available at http://localhost:8000
- API documentation: http://localhost:8000/docs (interactive Swagger UI)
- Alternative documentation: http://localhost:8000/redoc
- Can replace 8000 with any port you want

## Creating the Database Schema
To initialize the database schema:
```bash
python sql/create_schema.py # 
```

After executing the schema, it's a good idea to verify that everything was created correctly:
```bash
python sql/schema_check.py
```

## Data Migration
Data migration is the process of **transferring data from one system to another while** **ensuring data integrity** and **consistency**. Think of it like moving to a new house—you need to carefully pack (extract), potentially reorganize (transform), and then unpack (load) your belongings in the new location.

In our case, we're migrating from a simple storage system to a more sophisticated database design that includes additional tables and relationships.

To migrate data from the lightweight SQLite database (Task 3) to the new schema:
```bash
python -m app.database.migrations.migrate # or python app/database/migrations/migrate.py
```

## Running Tests
To run all tests:
```bash
pytest
```

To run all tests with verbose output:
```bash
pytest -v
```

To run specific test files:
```bash
pytest tests/test_api.py
pytest tests/test_models.py
pytest tests/test_database.py
pytest tests/test_error_handling.py
```

To run specific test functions, it follows the format: `pytest <path_to_test_file>::<TestClass>::<test_function>`:
```bash
# Example: test 'get_all_funds' function in TestDatabase class in test_database.py
pytest tests/test_database.py::TestDatabase::test_get_all_funds
```

## Project Structure
Directory structure:
```markdown
fund_management_system/
├── app/
│   ├── models/             # Data models
│   ├── api/                # API routes
│   ├── database/           # Database operations
│   │   └── migrations/     # Database migrations
│   └── utils/              # Utilities and error handlers
├── tests/                  # Test suite
├── docs/                   # Documentation
├── sql/                    # SQL schema definitions
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
└── README.md
```

In-Depth structure:
```markdown
fund_management_system/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── fund.py            # Task 1 - Fund model class
|   |   └── schemas.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # Task 2 - API endpoints
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py              # Task 3 - Database connection
│   │   ├── funds.db
|   |   |── fund_management.db
│   │   └── migrations/        # Task 5 - SQL migrations
│   │       └── migrate.py
│   └── utils/
│       ├── __init__.py
│       └── error_handlers.py  # Task 6 - Error handling
├── tests/                     # Task 7 - Test cases
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_models.py
│   ├── test_database.py
│   └── test_error_handling.py
├── sql/
│   ├── create_schema.py
│   ├── schema_check.py
│   └── schema.sql             # Task 4 - SQL schema
├── docs/                      # Task 8 - Documentation
│   ├── api_documentation.md
│   ├── database_documentation.md
│   └── Fund Management System ERD.png
├── requirements.txt
├── main.py                    # Application entry point
└── README.md
```

## API Endpoints
- `GET /api/funds/`: List all funds
- `POST /api/funds/`: Create a new fund
- `GET /api/funds/{fund_id}`: Get a specific fund
- `PATCH /api/funds/{fund_id}/performance`: Update a fund's performance
- `DELETE /api/funds/{fund_id}`: Delete a fund

For detailed API documentation, see [docs/api_documentation.md](https://github.com/mingjun1120/fund_management_system/blob/main/docs/api_documentation.md).

## Database Schema
The system uses a relational database with tables for funds, fund managers, categories, and performance history.

For detailed database documentation, see [docs/database_documentation.md](https://github.com/mingjun1120/fund_management_system/blob/main/docs/database_documentation.md).