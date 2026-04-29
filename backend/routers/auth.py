from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import create_access_token, get_db
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse
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
