from fastapi import FastAPI
from pydantic import BaseModel,Field

app = FastAPI()

class Address(BaseModel):
    city: str
    state: str
    pincode: int

class LoanApplication(BaseModel):
    applicant_name: str = Field(min_length=3,max_length=50)
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



loan_applications = [
    {
        "application_id": 1,
        "applicant_name": "Rahul",
        "loan_type": "Personal Loan",
        "loan_amount": 500000,
        "loan_status": "Pending"
    },
    {
        "application_id": 2,
        "applicant_name": "Amit",
        "loan_type": "Home Loan",
        "loan_amount": 1000000,
        "loan_status": "Pending"
    },
    {
        "application_id": 3,
        "applicant_name": "Priya",
        "loan_type": "Education Loan",
        "loan_amount": 300000,
        "loan_status": "Pending"
    }
]

@app.get("/")
def home():
    return {"message": "Hello"}

@app.get("/loan-applications/search")
def search_loan_applications(loan_type: str = None):

    result = []

    for loan in loan_applications:
        if loan_type is None or loan["loan_type"].lower() == loan_type.lower():
            result.append(loan)

    return result  

@app.get("/loan-applications", response_model=list[LoanResponse])
def get_loan_applications():
    return loan_applications

@app.get("/loan-applications/{application_id}")
def get_single_loan_application(application_id: int):

    for loan in loan_applications:
        if loan["application_id"]== application_id:
            return loan

    return {"message":"Loan app not found"}

def customer_loan(name:str , amount:int):
    return {
        "customer_name":name,
        "loan_amount":amount
    }

@app.post("/loan-applications", response_model=LoanResponse)
def create_loan(loan: LoanApplication):
    return {
        "application_id": 101,
        "applicant_name": loan.applicant_name,
        "loan_type": loan.loan_type,
        "loan_amount": loan.loan_amount,
        "loan_status": "Pending",
        "internal_notes": "Verification not completed"
    }

result = customer_loan("Amit",60000)
print(result)
    
