from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str
    state: str
    pincode: int


class LoanApplication(BaseModel):
    applicant_name: str = Field(min_length=3, max_length=50)
    middle_name: str | None = None
    loan_type: str
    loan_amount: float = Field(gt=0)
    address: Address


class LoanResponse(BaseModel):
    application_id: int
    applicant_name: str
    loan_type: str
    loan_amount: float
    loan_status: str

class LoanStatusUpdate(BaseModel):
    loan_status: str    



