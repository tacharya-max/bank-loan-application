from fastapi import FastAPI
from routers.loan_applications import router as loan_router
from routers.loan_status import router as status_router

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello"}


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