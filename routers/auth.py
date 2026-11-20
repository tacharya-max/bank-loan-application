from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError

from database import get_db
from models.user import User
from schemas.auth_schema import UserSignup, UserResponse, UserLogin, TokenResponse,RefreshTokenRequest,LogoutRequest
from utils.security import hash_password, verify_password
from utils.token import create_access_token, create_refresh_token,verify_refresh_token,verify_access_token
from utils.auth_dependency import get_current_user
from datetime import datetime, timezone
from utils.redis_client import blacklist_token, is_token_blacklisted
from fastapi.security import OAuth2PasswordRequestForm
from utils.auth_dependency import get_current_user, oauth2_scheme

router = APIRouter()

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    user_data: UserSignup,
    db: Session = Depends(get_db)
):

    # if email already exists
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registerd"
        )

    new_user = User(
        full_name = user_data.full_name,
        email = user_data.email,
        phone = user_data.phone,
        hashed_password = hash_password(user_data.password)
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.post("/login", response_model=TokenResponse)
def login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == login_data.username
    ).first()

    if not user or not verify_password(
        login_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    token_data = {
        "sub": str(user.id),
        "role": user.role
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



@router.get("/me",response_model=UserResponse)
def get_my_profile(
        current_user: User = Depends(get_current_user)
):
    return current_user    


@router.post("/refresh")
def refresh_access_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    if is_token_blacklisted(token_data.refresh_token):
        raise HTTPException(
        status_code=401,
        detail="Refresh token has been revoked. Please login again."
    )
    payload = verify_refresh_token(token_data.refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token payload"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive"
        )

    new_access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(
    token_data: LogoutRequest,
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user)
):
    access_token = token
    refresh_token = token_data.refresh_token

    access_payload = verify_access_token(access_token)
    refresh_payload = verify_refresh_token(refresh_token)

    if access_payload is None or refresh_payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if access_payload.get("sub") != str(current_user.id) or \
       refresh_payload.get("sub") != str(current_user.id):
        raise HTTPException(
            status_code=401,
            detail="Tokens do not belong to the logged-in user"
        )

    current_time = datetime.now(timezone.utc).timestamp()

    access_expiry = int(access_payload["exp"])
    refresh_expiry = int(refresh_payload["exp"])

    access_remaining = access_expiry - int(current_time)
    refresh_remaining = refresh_expiry - int(current_time)

    if access_remaining > 0:
        blacklist_token(access_token, access_remaining)

    if refresh_remaining > 0:
        blacklist_token(refresh_token, refresh_remaining)

    return {
        "message": "Successfully logged out"
    }