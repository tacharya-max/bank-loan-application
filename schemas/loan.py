from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Literal

class Address(BaseModel):
    city: str
    state: str
    pincode: str = Field(min_length=6, max_length=6)


class LoanCreate(BaseModel):
    loan_type: str
    loan_amount: Decimal = Field(gt=0)
    address: Address


class LoanResponse(BaseModel):
    model_config = {"from_attributes": True}
    application_id: int
    user_id: int
    loan_type: str
    loan_amount: Decimal
    loan_status: str
    city: str
    state: str
    pincode: str

class LoanUpdate(BaseModel):
    loan_type: str | None = None
    loan_amount: Decimal | None = Field(default=None, gt=0)  
    address: Address | None = None  

class LoanStatusUpdate(BaseModel):
    loan_status: Literal["pending", "Approved", "Rejected"]    



