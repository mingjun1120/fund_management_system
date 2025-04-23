from enum import Enum

class DatabaseType(Enum):
    SQLITE = "sqlite"
    JSON = "json" # We do not support JSON currently, you can add it if you want by creating all the necessary functions

# Set the database type here
ACTIVE_DATABASE = DatabaseType.SQLITE