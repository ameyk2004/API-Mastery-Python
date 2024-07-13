from typing import Optional
from pydantic import BaseModel,EmailStr

class UserOut(BaseModel):
    id:int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    owner: UserOut

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_data: str
    

class TokenData(BaseModel):
    id: Optional[int] = None