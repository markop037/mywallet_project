import os

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from jose import jwt as jose_jwt
from sqlalchemy.orm import Session

from dependencies import create_access_token, get_db
from schemas.auth import GoogleAuthRequest, LoginRequest, RegisterRequest, TokenResponse
from services.auth_service import AuthService

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    svc = AuthService(db)
    success, msg = svc.register_user(
        data.first_name, data.last_name,
        data.username, data.password, data.email,
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    return {"message": msg}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    svc = AuthService(db)
    if not svc.check_user_password(data.username, data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token({"sub": data.username})
    return TokenResponse(access_token=token)


@router.post("/google", response_model=TokenResponse)
def google_auth(data: GoogleAuthRequest, db: Session = Depends(get_db)):
    secret = os.environ.get("JWT_SECRET", "change-me-to-a-long-random-string")
    try:
        payload = jose_jwt.decode(
            data.access_token,
            secret,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Supabase token",
        )

    email: str = payload.get("email", "")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No email found in token",
        )

    meta = payload.get("user_metadata") or {}
    full_name = meta.get("full_name") or meta.get("name") or ""

    svc = AuthService(db)
    user = svc.get_or_create_oauth_user(email, full_name)
    token = create_access_token({"sub": user.Username})
    return TokenResponse(access_token=token)
