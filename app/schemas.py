from pydantic import BaseModel,EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id:int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True