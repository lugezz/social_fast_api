from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# ------ USERS -----------------------------------------------------------------


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ------ TOKEN -----------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# ------ POSTS -----------------------------------------------------------------

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True


# class Vote(BaseModel):
#     post_id: int
#     # 1: Like - 0: Not
#     dir: conint(le=1)
