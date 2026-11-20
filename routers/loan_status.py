
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.loan_application import LoanApplication as LoanApplicationModel
from models.user import User
from utils.auth_dependency import get_current_user
from schemas.loan import LoanStatusUpdate, LoanResponse


router = APIRouter()


@router.get("/")
def get_all_loan_statuses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    loans = db.query(LoanApplicationModel).filter(
        LoanApplicationModel.user_id == current_user.id
    ).all()

    result = []

    for loan in loans:
        result.append({
            "application_id": loan.application_id,
            "loan_status": loan.loan_status
        })

    return result


@router.get("/{application_id}")
def get_loan_status(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    loan = db.query(LoanApplicationModel).filter(
        LoanApplicationModel.application_id == application_id,
        LoanApplicationModel.user_id == current_user.id
    ).first()

    if loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan status not found"
        )

    return {
        "application_id": loan.application_id,
        "loan_status": loan.loan_status
    }


@router.patch("/{application_id}/status", response_model=LoanResponse)
def update_loan_status(
    application_id: int,
    update: LoanStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["loan_officer", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update loan status"
        )

    existing_loan = db.query(LoanApplicationModel).filter(
        LoanApplicationModel.application_id == application_id
    ).first()

    if existing_loan is None:
        raise HTTPException(
            status_code=404,
            detail="Loan application not found"
        )

    existing_loan.loan_status = update.loan_status

    db.commit()
    db.refresh(existing_loan)

    return existing_loan
