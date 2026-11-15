from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class LoanApplication(Base):

    __tablename__ = "loan_applications"

    # Primary Key
    application_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Foreign Key
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Loan details
    loan_type = Column(String(50), nullable=False)

    loan_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    loan_status = Column(
        String(30),
        default="Pending",
        nullable=False
    )

    # Applicant address
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(6), nullable=False)

    # Application creation time
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Many Loan Applications -> One User
    user = relationship(
        "User",
        back_populates="loan_applications"
    )