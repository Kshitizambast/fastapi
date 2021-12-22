from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from pydantic.types import conint


###### Post Schema ######
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    user_id: int

class PostCreate(PostBase):
    pass




###### User Schema ######
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None