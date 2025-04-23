import os
import sqlite3

def create_database_schema():
    
    """Create the database schema for the Fund Management System."""
    # Path to the schema file
    schema_path = os.path.join("sql", "schema.sql")
    
    # Path for the new database
    db_path = os.path.join('app', 'database', 'fund_management.db')
    
    print(f"Creating database schema at {db_path}...")
    
    # Read the schema SQL
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)
        conn.commit()
    
    print("Database schema created successfully!")

# Execute the function
if __name__ == "__main__":
    create_database_schema()