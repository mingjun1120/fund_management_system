# Fund Management System Database Documentation

## Overview
The Fund Management System uses a relational database to store information about investment funds, fund managers, fund categories, and performance history. This document describes the database schema, including tables, relationships, and key constraints.

## Entity-Relationship Diagram
![Fund Management System ERD](../docs/Fund%20Management%20System%20ERD.png)

Note: A line connecting two entities represents a relationship where a record in one entity can be associated with one or more records in another entity.

## Database Tables
### funds
The primary table storing information about investment funds.

| Column         | Type    | Constraints      | Description                            |
|----------------|---------|------------------|----------------------------------------|
| fund_id        | TEXT    | PRIMARY KEY      | Unique identifier for the fund         |
| name           | TEXT    | NOT NULL, UNIQUE | Name of the fund                       |
| manager_name   | TEXT    | NOT NULL         | Name of the fund manager               |
| description    | TEXT    |                  | Description of the fund                |
| nav            | REAL    | NOT NULL, >= 0   | Net Asset Value of the fund           |
| creation_date  | TEXT    | NOT NULL         | Date when the fund was created (ISO8601)|
| performance    | REAL    | NOT NULL         | Fund's performance as a percentage     |
| last_updated   | TEXT    | NOT NULL         | Last update timestamp (ISO8601)        |

### fund_managers
Stores detailed information about fund managers.

| Column           | Type    | Constraints      | Description                            |
|------------------|---------|------------------|----------------------------------------|
| manager_id       | TEXT    | PRIMARY KEY      | Unique identifier for the manager      |
| name             | TEXT    | NOT NULL         | Name of the manager                    |
| email            | TEXT    | UNIQUE           | Manager's email address                |
| phone            | TEXT    |                  | Manager's phone number                 |
| qualification    | TEXT    |                  | Manager's qualifications               |
| years_experience | INTEGER | >= 0             | Years of experience in fund management |
| date_joined      | TEXT    | NOT NULL         | Date when the manager joined (ISO8601) |

### fund_categories
Defines categories for classifying funds.

| Column      | Type | Constraints      | Description                     |
|-------------|------|------------------|---------------------------------|
| category_id | TEXT | PRIMARY KEY      | Unique identifier for the category |
| name        | TEXT | NOT NULL, UNIQUE | Name of the category            |
| description | TEXT |                  | Description of the category     |

### fund_category_mappings
Junction table implementing the many-to-many relationship between funds and categories.

| Column      | Type | Constraints                                                | Description                |
|-------------|------|------------------------------------------------------------|-----------------------------|
| fund_id     | TEXT | PRIMARY KEY, FOREIGN KEY → funds(fund_id) ON DELETE CASCADE | Reference to the fund       |
| category_id | TEXT | PRIMARY KEY, FOREIGN KEY → fund_categories(category_id) ON DELETE CASCADE | Reference to the category  |

### fund_performance_history
Tracks historical performance values for funds over time.

| Column           | Type  | Constraints                                      | Description                          |
|------------------|-------|--------------------------------------------------|--------------------------------------|
| history_id       | TEXT  | PRIMARY KEY                                      | Unique identifier for the history record |
| fund_id          | TEXT  | NOT NULL, FOREIGN KEY → funds(fund_id) ON DELETE CASCADE | Reference to the fund             |
| performance_date | TEXT  | NOT NULL                                         | Date of the performance record (ISO8601) |
| performance_value| REAL  | NOT NULL                                         | Performance value as a percentage      |

A unique constraint ensures there is only one performance record per fund per date.

## Indexes
The following indexes improve query performance:

| Index Name                            | Table                      | Columns           | Purpose                                      |
|---------------------------------------|----------------------------|-------------------|----------------------------------------------|
| idx_funds_manager_name                | funds                      | manager_name      | Speed up queries that filter by manager name |
| idx_fund_performance_history_fund_id  | fund_performance_history   | fund_id           | Speed up queries for a fund's history        |
| idx_fund_performance_history_date     | fund_performance_history   | performance_date  | Speed up queries that filter by date         |

## Data Types
- **TEXT**: Used for string values and unique identifiers
- **REAL**: Used for floating-point numbers (NAV, performance)
- **INTEGER**: Used for whole numbers (years of experience)

Dates and timestamps are stored as ISO8601 formatted strings (e.g., "2025-01-01T00:00:00").

## Relationships
1. **Funds to Fund Managers**: One-to-many (implied through the `manager_name` field, one fund manager can manage multiple funds)
2. **Funds to Fund Categories**: Many-to-many (through the fund_category_mappings table)
3. **Funds to Performance History**: One-to-many (one fund can have multiple performance records)

## Constraints
1. **Primary Keys**: Ensure each record is uniquely identifiable
2. **Foreign Keys**: Maintain referential integrity between tables
3. **NOT NULL**: Ensure required fields are always provided
4. **UNIQUE**: Prevent duplicate values (e.g., fund names, category names)
5. **CHECK**: Validate data (e.g., NAV must be non-negative)
6. **ON DELETE CASCADE**: Automatically remove related records when a parent record is deleted

## Data Migrations
The system includes migration scripts to move data from a lightweight storage solution (SQLite database: `app\database\funds.db`) to this comprehensive schema (`app\database\fund_management.db`). The migration process:
1. Reads data from the source
2. Transforms it to match the new schema
3. Inserts it into the appropriate tables

## Accessing the Database
The database can be accessed through:
1. The API endpoints (recommended)
2. Direct database queries (for maintenance or advanced operations)

SQLite is used as the database engine, which stores all data in a single file (`fund_management.db`).

## NOTE! What the Migration Doesn't Cover
Note that our migration script focuses on core fund data. For a complete migration involving all tables in our schema, we would also need to:

1. Create fund categories
2. Extract or generate data for fund managers
3. Establish mappings between funds and categories

Since our original data model only contained basic fund information, we're focusing on migrating what we have. In a real-world scenario, we might need to gather additional data for the complete migration.