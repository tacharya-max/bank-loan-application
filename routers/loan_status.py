from fastapi import APIRouter, HTTPException
from routers.loan_applications import loan_applications

router = APIRouter()


@router.get("/")
def get_all_loan_statuses():
    result = []

    for loan in loan_applications:
        result.append({
            "application_id": loan["application_id"],
            "loan_status": loan["loan_status"]
        })

    return result


@router.get("/{application_id}")
def get_loan_status(application_id: int):

    for loan in loan_applications:
        if loan["application_id"] == application_id:
            return {
                "application_id": loan["application_id"],
                "loan_status": loan["loan_status"]
            }

    raise HTTPException(
        status_code=404,
        detail="Loan status not found"
    )