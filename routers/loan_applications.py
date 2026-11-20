
from fastapi import APIRouter, HTTPException,Response,Header,Cookie,Depends
from schemas.loan import LoanCreate, LoanResponse, LoanStatusUpdate, LoanUpdate
from sqlalchemy.orm import Session
from database import get_db
from models.loan_application import LoanApplication as LoanApplicationModel
from utils.auth_dependency import get_current_user
from models.user import User


router = APIRouter()




@router.get("/search", response_model=list[LoanResponse])
def search_loan_applications(
    loan_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(LoanApplicationModel)

    if current_user.role == "applicant":
        query = query.filter(
            LoanApplicationModel.user_id == current_user.id
        )

    elif current_user.role not in ["loan_officer", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to search loan applications"
        )

    if loan_type is not None:
        query = query.filter(
            LoanApplicationModel.loan_type.ilike(f"%{loan_type}%")
        )

    return query.all()



@router.get("/profile")
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role
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
def get_loan_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    loans = db.query(LoanApplicationModel).filter(
        LoanApplicationModel.user_id == current_user.id).all()
    return loans


@router.get("/{application_id}", response_model=LoanResponse)
def get_single_loan_application(
    application_id: int, db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    loan = db.query(LoanApplicationModel).filter(
        LoanApplicationModel.application_id == application_id,
        LoanApplicationModel.user_id == current_user.id
    ).first()

    if loan is None:

        raise HTTPException(
        status_code=404,
        detail="Loan application not found"
    )
    return loan




@router.post("/", response_model=LoanResponse, status_code=201)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    new_loan = LoanApplicationModel(
        user_id = current_user.id,
        loan_type = loan.loan_type,
        loan_amount = loan.loan_amount,
        loan_status = "Pending",
        city = loan.address.city,
        state = loan.address.state,
        pincode = loan.address.pincode
    )

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return new_loan



@router.put("/{application_id}", response_model=LoanResponse)
def replace_loan(
    application_id: int,
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user  : User = Depends(get_current_user)
):
    # Step 1: Find existing loan from database
    existing_loan = db.query(LoanApplicationModel).filter(
        LoanApplicationModel.application_id == application_id,
        LoanApplicationModel.user_id == current_user.id
    ).first()

    if existing_loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    existing_loan.loan_type = loan.loan_type
    existing_loan.loan_amount = loan.loan_amount
    existing_loan.city = loan.address.city
    existing_loan.state = loan.address.state
    existing_loan.pincode = loan.address.pincode

   
    db.commit()
    db.refresh(existing_loan)
    return existing_loan
    



@router.patch("/{application_id}", response_model=LoanResponse)
def update_loan_application(
    application_id: int,
    loan: LoanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_loan = db.query(LoanApplicationModel).filter(
        LoanApplicationModel.application_id == application_id,
        LoanApplicationModel.user_id == current_user.id
    ).first()

    if existing_loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    update_data = loan.model_dump(exclude_unset=True)

    if "address" in update_data:
        address = update_data.pop("address")

        if address is not None:
            existing_loan.city = address["city"]
            existing_loan.state = address["state"]
            existing_loan.pincode = address["pincode"]

    for field, value in update_data.items():
        if value is not None:
            setattr(existing_loan, field, value)

    db.commit()
    db.refresh(existing_loan)

    return existing_loan



@router.delete("/{application_id}", status_code=204)
def delete_loan(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_loan = db.query(LoanApplicationModel).filter(
        LoanApplicationModel.application_id == application_id,
        LoanApplicationModel.user_id == current_user.id
    ).first()

    if existing_loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    db.delete(existing_loan)
    db.commit()

    return Response(status_code=204)

        



