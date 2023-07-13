from pydantic import BaseModel


class Post(BaseModel):
    """A blog post"""
    author_id: int
    content: str
    title: str


class User(BaseModel):
    """A user"""
    email: str
    password: str
    is_admin: bool
