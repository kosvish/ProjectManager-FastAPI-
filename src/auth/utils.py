from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.config import SECRET_KEY, ALGORYTHM
from src.database import get_db
from src.auth.schemas import UserInDB, TokenData
from src.auth.schemas import User as UserSchema
from sqlalchemy.orm import Session
from src.auth.models import User

ACCESS_TOKEN_EXPIRE_MINUTE = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user is not None:
        return UserSchema(id=user.id, username=user.username,
                          email=user.email, password=user.hashed_password,
                          authenticated=user.authenticated,
                          role_id=user.role_id, role=user.role.role_name)


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)
    return encode_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(token_data.username, get_db())
    if user is None:
        raise credentials_exception
    return user
