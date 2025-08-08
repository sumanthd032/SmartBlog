import datetime
from pydantic import BaseModel

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
        orm_mode = True