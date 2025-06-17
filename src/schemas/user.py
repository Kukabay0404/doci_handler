from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password : str

class CreateAdmin(BaseModel):
    email: EmailStr
    password : str
    is_admin: Optional[bool] = 0

class UserRead(BaseModel):
    id : int
    email : EmailStr
    is_active : bool
    is_admin : bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str