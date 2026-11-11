
from fastapi import APIRouter, HTTPException,Response,Header,Cookie
from schemas.loan import LoanApplication, LoanResponse, LoanStatusUpdate

router = APIRouter()


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


@router.get("/search")
def search_loan_applications(loan_type: str = None):

    result = []

    for loan in loan_applications:
        if loan_type is None or loan["loan_type"].lower() == loan_type.lower():
            result.append(loan)

    return result

@router.get("/profile")
def get_profile(authorization: str = Header(None)):
    return {
        "authorization_token": authorization
    }


@router.get("/info")
def get_info(response: Response):
    response.headers["X-App-Name"] = "Bank Loan API"

    return {
        "message": "Application information"
    }

@router.get("/login")
def login(response: Response):
    response.set_cookie(
        key="user_token",
        value="abc123",
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return{
        "message":"Login successful"
    }

@router.get("/check-cookie")
def check_cookie(user_token: str = Cookie(None)):
    return{
        "user_token": user_token
    }


@router.get("/", response_model=list[LoanResponse])
def get_loan_applications():
    return loan_applications


@router.get("/{application_id}", response_model=LoanResponse)
def get_single_loan_application(application_id: int):

    for loan in loan_applications:
        if loan["application_id"] == application_id:
            return loan

    raise HTTPException(
        status_code=404,
        detail="Loan application not found"
    )




@router.post("/", response_model=LoanResponse, status_code=201)
def create_loan(loan: LoanApplication):

    new_loan = {
        "application_id": 101,
        "applicant_name": loan.applicant_name,
        "loan_type": loan.loan_type,
        "loan_amount": loan.loan_amount,
        "loan_status": "Pending",
        "internal_notes": "Verification not completed"
    }

    loan_applications.append(new_loan)

    return new_loan


@router.put("/{application_id}")
def replace_loan(application_id: int, loan: LoanApplication):

    for index,existing_loan in enumerate(loan_applications):

        if existing_loan["application_id"] == application_id:

            updated_loan = {
                "application_id": application_id,
                "applicant_name": loan.applicant_name,
                "loan_type": loan.loan_type,
                "loan_amount": loan.loan_amount,
                "loan_status": existing_loan["loan_status"],
                "address": loan.address.model_dump()
            }

            loan_applications[index] = updated_loan
            return updated_loan

    raise HTTPException(
        status_code=404,
        detail="Loan application not found"
    )    


@router.patch("/{application_id}/status")
def update_loan_status(
    application_id:int,
    update: LoanStatusUpdate
):
    for loan in loan_applications:

        if loan["application_id"] == application_id:
            loan["loan_status"] = update.loan_status
            return loan

    raise HTTPException(
        status_code=404,
        detail="Loan application not found"
    )


@router.delete("/{application_id}", status_code=204)
def delete_loan(application_id: int):

    for index, loan in enumerate(loan_applications):
        if loan["application_id"] == application_id:
            loan_applications.pop(index)
            return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail="Loan application not found"
    )       



