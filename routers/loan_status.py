
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.loan_application import LoanApplication as LoanApplicationModel

router = APIRouter()


@router.get("/")
def get_all_loan_statuses(db: Session = Depends(get_db)):
    loans = db.query(LoanApplicationModel).all()

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
    db: Session = Depends(get_db)
):
    loan = db.query(LoanApplicationModel).filter(
        LoanApplicationModel.application_id == application_id
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
