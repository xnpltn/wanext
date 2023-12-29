from fastapi import APIRouter, Depends, HTTPException, status
from app import schema
from app.database import connect_db
from sqlalchemy.orm import Session
from utils import crud

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)





@router.post("/signup")
async def signup(user: schema.UserCreate, db: Session = Depends(connect_db)):
    user_query = crud.get_user_by_email(db, email=user.email)
    print(user_query.first())
    if user_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user With that Email Already Exists")
    return crud.create_user(db=db, user=user)


@router.post("/login")
async def login(user: schema.UserLogin, db: Session = Depends(connect_db)):
    user_query = crud.get_user_by_email(db, email=user.email)
    if not user_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    return {'message': 'Login is Successful'}