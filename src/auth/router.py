from fastapi import APIRouter, Depends, status, HTTPException
from src.auth.schemas import CreateUser, LoginUser, UserResponse, UserInDB
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.models import User as UserModel
from src.auth.utils import (get_password_hash, oauth2_scheme, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTE,
                            create_access_token)
from src.auth.schemas import Token
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta


router = APIRouter(
    prefix="/auth",
    tags=["User"]
)


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def user_register(user: CreateUser, db: Session = Depends(get_db)):
    user_email = db.query(UserModel).filter(user.email == UserModel.email).first()
    if user_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email already exists")

    password = get_password_hash(user.password)
    new_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=password,
        authenticated=False,
        role_id=1,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Привязываем объект к сессии
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return UserResponse(
        username=new_user.username,
        email=new_user.email,
        hashed_password=new_user.hashed_password,
    )


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticated": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/login", response_model=UserInDB)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, Depends(get_db))
    if user is None or user is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticated": "Bearer"}
        )

    return user


