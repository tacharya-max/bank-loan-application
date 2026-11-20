
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db
from models.user import User
from models.loan_application import LoanApplication

from routers.loan_applications import router as loan_router
from routers.loan_status import router as status_router
from routers.auth import router as auth_router


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello"}


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):

    result = db.execute(text("SELECT 1"))

    return {
        "message": "Database connected successfully",
        "database_result": result.scalar()
    }


app.include_router(
    loan_router,
    prefix="/loan-applications",
    tags=["Loan Applications"]
)


app.include_router(
    status_router,
    prefix="/loan-status",
    tags=["Loan status"]
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)
