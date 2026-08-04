from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.jwt import create_access_token
from app.core.security import hash_password
from app.core.security import verify_password
from app.db.session import get_db
from app.models.member import Member
from app.schema.request.auth import LoginRequest, RegisterRequest
from app.schema.response.auth import (
    LoginResponse,
    LoginResponseData,
    RegisterResponse,
    RegisterResponseData,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=RegisterResponse)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    name = payload.name.strip()
    password = payload.password.strip()

    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name is required",
        )

    if not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required",
        )

    existing_user = db.query(Member).filter(Member.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    try:
        user = Member(
            name=name,
            email=email,
            password=hash_password(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register user",
        )

    return RegisterResponse(
        status=200,
        message="User registered successfully",
        data=RegisterResponseData(
            id=user.id,
            name=user.name,
            email=user.email,
        ),
    )


@router.post("/login", response_model=LoginResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    password = payload.password.strip()

    user = db.query(Member).filter(Member.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        subject=str(user.id),
        user_id=user.id,
        email=user.email,
    )

    return LoginResponse(
        status=200,
        message="user login successful",
        data=LoginResponseData(
            id=user.id,
            name=user.name,
            email=user.email,
            access_token=access_token,
        ),
    )
