import os
import sqlite3

def check_database_structure():
    """Verify the database structure was created properly."""
    
    # Path for the new database
    db_path = os.path.join('app', 'database', 'fund_management.db')
    
    with sqlite3.connect(db_path) as conn:
        # Get list of tables
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print("Tables in database:", tables)
        
        # For each table, get its column info
        for table in tables:
            print(f"\nColumns in {table} table:")
            cursor = conn.execute(f"PRAGMA table_info({table});")
            for column in cursor.fetchall():
                cid, name, type_, notnull, default_value, pk = column
                print(f"  - {name} ({type_}){' PRIMARY KEY' if pk else ''}{' NOT NULL' if notnull else ''}")

if __name__ == "__main__":
    check_database_structure()