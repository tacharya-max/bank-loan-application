from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):

    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # User details
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(15), nullable=True)

    # Authentication details
    hashed_password = Column(String, nullable=False)

    # User role
    role = Column(String(30), default="applicant", nullable=False)

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)

    # Account creation time
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # One User -> Many Loan Applications
    loan_applications = relationship(
        "LoanApplication",
        back_populates="user"
    )