
import os
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
)

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing in .env")


# Create Access Token
def create_access_token(data: dict) -> str:

    token_data = data.copy()
    token_data["type"] = "access"

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token_data["exp"] = expire

    return jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Create Refresh Token
def create_refresh_token(data: dict) -> str:

    token_data = data.copy()
    token_data["type"] = "refresh"

    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    token_data["exp"] = expire

    return jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Verify Access Token
def verify_access_token(token: str) -> dict | None:

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "access":
            return None

        return payload

    except JWTError:
        return None


# Verify Refresh Token
def verify_refresh_token(token: str) -> dict | None:

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            return None

        return payload

    except JWTError:
        return None
