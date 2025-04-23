from pydantic import BaseModel, Field
from datetime import datetime

class FundBase(BaseModel):
    """Base model with shared attributes."""
    name: str = Field(..., min_length=1, description="Name of the fund")
    manager_name: str = Field(..., min_length=1, description="Name of the fund manager")
    description: str = Field(..., description="Description of the fund")
    nav: float = Field(..., gt=0, description="Net Asset Value of the fund")
    performance: float = Field(..., description="Fund performance as a percentage")

class FundCreate(FundBase):
    """Model for creating a new fund."""
    pass

class FundUpdate(BaseModel):
    """Model for updating a fund's performance."""
    performance: float = Field(..., description="Updated fund performance percentage")

class FundResponse(FundBase):
    """Model for fund responses, including all attributes."""
    fund_id: str
    creation_date: datetime

    class Config:
        """Pydantic config."""
        from_attributes = True  # Allow ORM model -> Pydantic model conversion