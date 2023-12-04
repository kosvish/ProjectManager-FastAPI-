from fastapi import APIRouter, Depends, status, HTTPException
from src.auth.schemas import CreateUser, LoginUser, UserResponse
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.models import User as UserModel
from src.utils import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["User"]
)


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def user_register(user: CreateUser, db: Session = Depends(get_db)):
    user_email = db.query(UserModel).filter(user.email == UserModel.email).first()
    if user_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email already exists")

    password = hash_password(user.password)
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
