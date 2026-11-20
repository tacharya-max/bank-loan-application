
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from utils.token import verify_access_token
from utils.redis_client import is_token_blacklisted

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked. Please login again."
        )

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive"
        )

    return user
