from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(Post):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True



    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str


class UserCreate(User):
    pass


class UserLogin(User):
    pass


class Token(BaseModel):
    token_type: str
    access_token: str


class TokenData(BaseModel):
    id: Optional[str] = None


class VoteResponse(BaseModel):
    post_id: int
    dir: conint(le=1)
