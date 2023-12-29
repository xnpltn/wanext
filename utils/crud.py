from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import models, schema
from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app import schema
from .encryptor import *
from utils.oauth2 import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

async def create_user(db: Session, user: schema.UserCreate):
    user_query  = db.query(models.User).filter(models.User.email == user.email).first()
    username_query =  db.query(models.User).filter(models.User.username == user.username).first()

    if user_query is None:
        if username_query is None:
            user.password = hash_pwd(user.password)
            new_user = models.User(**user.model_dump())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{user.username} is taken")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"user with {user.email} already exits")

# def login_user(db: Session, user: schemas.UserLogin, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
async def login_user(db: Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_query  = db.query(models.User).filter(models.User.email == form_data.username).first()

    if user_query is not None:
        if verify_pwd(form_data.password, user_query.password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "Bearer"}
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password or email")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with{form_data.username} does't exist")
