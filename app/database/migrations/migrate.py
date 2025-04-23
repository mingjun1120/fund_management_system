import os
import sqlite3
import json
import uuid
from datetime import datetime
from app.config import DatabaseType, ACTIVE_DATABASE

# Paths for databases
SOURCE_DB_PATH = os.path.join("app", "database", "funds.db") if ACTIVE_DATABASE == DatabaseType.SQLITE else "funds.json"
TARGET_DB_PATH = os.path.join("app", "database", "fund_management.db")

def migrate_data():
    """
    Migrate data from the lightweight database to the comprehensive SQL database.
    """
    print(f'Starting migration from "{SOURCE_DB_PATH}" to "{TARGET_DB_PATH}"...')
    
    # Step 1: Read data from the source database
    if ACTIVE_DATABASE == DatabaseType.SQLITE:
        source_data = read_from_sqlite()
    else:
        source_data = read_from_json()
    
    print(f"Read {len(source_data)} funds from source database.")
    
    # Step 2: Connect to the target database
    with sqlite3.connect(TARGET_DB_PATH) as target_conn:
        # Enable foreign keys
        target_conn.execute("PRAGMA foreign_keys = ON")
        
        # Step 3: Migrate the data
        migrate_funds(target_conn, source_data)
        migrate_performance_history(target_conn, source_data)
        
        # Commit the changes
        target_conn.commit()
    
    print("Migration completed successfully!")

def read_from_sqlite():
    """
    Read fund data from the SQLite source database.
    """
    funds = []
    
    with sqlite3.connect(SOURCE_DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM funds')
        rows = cursor.fetchall()
        
        for row in rows:
            # Convert row to dictionary
            fund = dict(row)
            funds.append(fund)
    
    return funds

def read_from_json():
    """
    Read fund data from the JSON source file.
    """
    with open(SOURCE_DB_PATH, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # If the file is empty or invalid JSON
            return []

def migrate_funds(target_conn, source_data):
    """
    Migrate fund data to the funds table in the target database.
    
    Args:
        target_conn: Connection to the target database
        source_data: List of fund dictionaries from the source database
    """
    cursor = target_conn.cursor()
    
    # Before inserting, check if there's existing data to avoid duplicates
    cursor.execute("SELECT COUNT(*) FROM funds")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"Warning: Target database already contains {existing_count} funds.")
        response = input("Do you want to continue and potentially create duplicates? (y/n): ")
        if response.lower() != 'y':
            print("Migration cancelled.")
            return
    
    # Insert each fund into the target database
    for fund in source_data:
        # Ensure we have all required fields with proper types
        fund_id = fund.get('fund_id', str(uuid.uuid4()))
        name = fund.get('name', '')
        manager_name = fund.get('manager_name', '')
        description = fund.get('description', '')
        nav = float(fund.get('nav', 0.0))
        
        # Handle creation_date (might be a string or datetime object)
        creation_date = fund.get('creation_date')
        if isinstance(creation_date, datetime):
            creation_date = creation_date.isoformat()
        elif not creation_date:
            creation_date = datetime.now().isoformat()
        
        performance = float(fund.get('performance', 0.0))
        last_updated = datetime.now().isoformat()
        
        try:
            cursor.execute('''
                INSERT INTO funds 
                (fund_id, name, manager_name, description, nav, creation_date, performance, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                fund_id, name, manager_name, description, nav, 
                creation_date, performance, last_updated
            ))
            print(f"Migrated fund: {name}")
        except sqlite3.IntegrityError as e:
            print(f"Error migrating fund {name}: {e}")

def migrate_performance_history(target_conn, source_data):
    """
    Create initial performance history entries for each fund.
    
    Args:
        target_conn: Connection to the target database
        source_data: List of fund dictionaries from the source database
    """
    cursor = target_conn.cursor()
    
    # For each fund, create an initial performance history entry
    for fund in source_data:
        fund_id = fund.get('fund_id')
        performance = float(fund.get('performance', 0.0))
        
        # Use either the fund's creation date or today as the performance date
        creation_date = fund.get('creation_date')
        if isinstance(creation_date, datetime):
            performance_date = creation_date.isoformat()
        elif isinstance(creation_date, str):
            performance_date = creation_date
        else:
            performance_date = datetime.now().isoformat()
        
        # Generate a unique ID for the history record
        history_id = str(uuid.uuid4())
        
        try:
            cursor.execute('''
                INSERT INTO fund_performance_history 
                (history_id, fund_id, performance_date, performance_value)
                VALUES (?, ?, ?, ?)
            ''', (
                history_id, fund_id, performance_date, performance
            ))
            print(f"Created performance history for fund ID: {fund_id}")
        except sqlite3.IntegrityError as e:
            print(f"Error creating performance history for fund ID {fund_id}: {e}")

if __name__ == "__main__":
    migrate_data()