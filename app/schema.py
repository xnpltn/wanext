from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    

class UserCreate(User):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str