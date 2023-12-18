from fastapi import APIRouter, BackgroundTasks, Response, Cookie, status, HTTPException, Depends
from src.database import get_db
from src.auth.models import User as UserModel
from src.auth.utils import get_user, decode_user_token
from sqlalchemy.orm import Session
from sqlalchemy import update
from .service import send_email_verification

router = APIRouter(
    prefix="/verification"
)


@router.get("", status_code=status.HTTP_200_OK)
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


@router.get("/email")
def get_verification_email(background_tasks: BackgroundTasks, user_data: str | None = Cookie(default=None),
                           db: Session = Depends(get_db)):
    token_data = decode_user_token(user_data)
    username = token_data["sub"]
    current_user = get_user(username, db)
    if current_user is None or current_user is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    background_tasks.add_task(send_email_verification, current_user.email, user_data)
    return {"message": "A verification letter has been sent to your email."}



