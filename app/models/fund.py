from uuid import uuid4
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Fund:
    """
    Represents an investment fund in the system.
    
    Attributes:
        fund_id (str): Unique identifier for the fund
        name (str): Name of the investment fund
        manager_name (str): Name of the fund manager
        description (str): Description of the fund's purpose or strategy
        nav (float): Net Asset Value of the fund
        creation_date (datetime): Date when the fund was created
        performance (float): Fund's performance as a percentage
    """
    name: str
    manager_name: str
    description: str
    nav: float
    performance: float
    # Auto-generated fields with defaults
    fund_id: str = field(default_factory=lambda: str(uuid4()))
    creation_date: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate the fund data after initialization."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Fund name must be a non-empty string")
        
        if not self.manager_name or not isinstance(self.manager_name, str):
            raise ValueError("Fund manager name must be a non-empty string")
        
        if not isinstance(self.description, str):
            raise ValueError("Fund description must be a string")
        
        if not isinstance(self.nav, (int, float)) or self.nav < 0:
            raise ValueError("Fund NAV must be a non-negative number")
        
        if not isinstance(self.performance, (int, float)):
            raise ValueError("Fund performance must be a number")
    
    def to_dict(self) -> dict:
        """Convert the Fund object to a dictionary for serialization."""
        return {
            "fund_id": self.fund_id,
            "name": self.name,
            "manager_name": self.manager_name,
            "description": self.description,
            "nav": self.nav,
            "creation_date": self.creation_date.isoformat(),
            "performance": self.performance
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Fund':
        """Create a Fund object from a dictionary."""
        # Handle the creation_date which needs to be parsed from string to datetime
        if isinstance(data.get('creation_date'), str):
            data['creation_date'] = datetime.fromisoformat(data['creation_date'])
        
        return cls(**data)