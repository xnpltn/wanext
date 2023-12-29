from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import schema
from app.database import connect_db
from sqlalchemy.orm import Session
from utils.crud import create_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)





@router.post("/signup")
async def signup(user: schema.UserCreate ,db: Session = Depends(connect_db)):
    return await create_user(db=db, user=user)
    

# user: schemas.UserLogin
@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(connect_db)):
    return await login_user(db=db, form_data=form_data)