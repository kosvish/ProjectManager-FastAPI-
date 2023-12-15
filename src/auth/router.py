from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException, Response, Cookie
from src.auth.schemas import CreateUser, UserResponse, UserInDB
from sqlalchemy.orm import Session
from sqlalchemy import update, values
from src.database import get_db
from src.auth.models import User as UserModel
from src.auth.utils import (get_password_hash, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTE,
                            create_access_token, verify_access_token, decode_user_token, get_user)

from fastapi.security import OAuth2PasswordRequestForm
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
        email=new_user.email
    )


@router.post("/login", response_model=UserResponse)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticated": "Bearer"}
        )
    access_token_expires = timedelta(days=7)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    cookie_expire_data = datetime.utcnow() + timedelta(days=7)
    cookie_expire_data_unix = int(cookie_expire_data.timestamp())
    response.set_cookie(key="user_data", value=access_token,
                        expires=cookie_expire_data_unix)

    return user


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response, user_data: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You should login before logout")
    decode_user_data = verify_access_token(user_data, db)
    response.delete_cookie(key="user_data")
    return {"message": "Success"}


@router.post("/verification", status_code=status.HTTP_200_OK)
def verification(response: Response, user_data: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    token_data = decode_user_token(user_data)
    username = token_data["sub"]
    current_user = get_user(username, db)
    if current_user is None or current_user is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    current_user.authenticated = True

    stmt = (
        update(UserModel)
        .values(authenticated=True)
        .where(UserModel.username == current_user.username)
    )
    db.execute(stmt)

    db.commit()

    return {"message": "You have successfully authenticated"}
