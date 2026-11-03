from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanApplication(BaseModel):
    applicant_name: str
    loan_amount: int
    loan_type: str

loan_applications = [
    {
        "application_id": 1,
        "applicant_name": "Rahul",
        "loan_type": "Personal Loan",
        "loan_amount": 500000
    },
    {
        "application_id": 2,
        "applicant_name": "Amit",
        "loan_type": "Home Loan",
        "loan_amount": 1000000
    },
    {
        "application_id": 3,
        "applicant_name": "Priya",
        "loan_type": "Education Loan",
        "loan_amount": 300000
    }
]

@app.get("/")
def home():
    return {"message": "Welcome to Bank Loan Application"}

@app.get("/loan-applications/search")
def search_loan_applications(loan_type: str = None):

    result = []

    for loan in loan_applications:
        if loan_type is None or loan["loan_type"].lower() == loan_type.lower():
            result.append(loan)

    return result  

@app.get("/loan-applications")
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

result = customer_loan("Amit",60000)
print(result)
    


@app.post("/loan-applications")
def create_loan_application(loan:LoanApplication):
    return {
        "message":"Loan app received",
        "application":loan
    }