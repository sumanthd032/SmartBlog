import datetime
from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentAuthor(BaseModel): 
    username: str
    class Config:
        from_attributes = True

class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime.datetime
    author: CommentAuthor 

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str | None = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime.datetime
    comments: list[Comment] = [] 

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    posts: list[Post] = []
    comments: list[Comment] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class AIRequest(BaseModel):
    content: str
