from datetime import datetime, timedelta
from jose import JWTError, jwt
from app import schema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import connect_db
from app import models




SECRET_KEY = "fbefc4e2e8b01bc49d7a116893717b82cb4eca2a1c9b8232920f617f7123dcd3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(connect_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.username)
    if user is None:
        raise credentials_exception
    return user

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if id is None:
            raise credential_exception
        token_data = schema.TokenData(username=username)
    except JWTError as exc:
        raise credential_exception
    return token_data


def get_current_user(token:str = Depends(OAuth2PasswordBearer(tokenUrl="login")), db : Session = Depends(connect_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token =  verify_access_token(token=token, credential_exception=credential_exception)
    user = db.query(models.User).filter(models.User.email == token.username).first()

    return user