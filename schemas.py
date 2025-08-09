import datetime
from pydantic import BaseModel

# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: str | None = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# --- User Schemas (NEW) ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    posts: list[Post] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class AIRequest(BaseModel):
    content: str