from fastapi import APIRouter, Depends, HTTPException, Request
import random
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_db
from app.core.models import Token, OtpModel
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user, verify_password
from sqlalchemy.orm import Session
import fastapi
from app.api.exceptions import credentials_exception
from . import send_email
from app.crud.crud_base import CRUDBase
from pydantic import EmailStr
from app.crud.crud_users import crud_users
from app.models import Token, User
from app.schemas.users import UserCreate, UserUpdate, UserRead


router = fastapi.APIRouter(tags=["login"])


@router.post("/login", status_code=200)
async def login_user(db: Annotated[Session, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise credentials_exception

    user_email_otp = db.query(Token).filter(
        Token.email == form_data.username).first()
    if user_email_otp:
        db.delete(user_email_otp)
        db.commit()

    # if not user["is_superuser"]:
    #

    otp_token = random.randint(100000, 999999)

    otp_row = Token(email=user["email"], token=otp_token)
    db.add(otp_row)
    db.commit()

    await send_email.send_email(subject="Welcome to FastAPI app", email_to=form_data.username, body={"name": user["name"], "token": otp_token})

    return {"message": "OTP sent successfully"}


@router.post("/verify_otp", status_code=200)
async def verify_otp_code(otp_code: int, db: Annotated[Session, Depends(get_db)], email: EmailStr):

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    otp_row = db.query(Token).filter(Token.token == str(otp_code)).first()

    if not otp_row:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_row.email != email:
        raise HTTPException(status_code=400, detail="Invalid Email")

    if otp_row.token != str(otp_code):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # delete otp from database
    db.delete(otp_row)
    db.commit()

    # print()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )

    user_dict = UserRead.from_orm(user)

    return {"access_token": access_token, "token_type": "bearer", "user": user_dict}

    # return {"message": "OTP verified successfully"}

# @router.post("/resend-")
