from pydantic import BaseModel


class Post(BaseModel):
    """A blog post"""
    user_id: int
    image_url: str
    content: str
    title: str
    description: str


class User(BaseModel):
    """A user"""
    email: str
    password: str
    is_admin: bool
    bio: str
    name: str


class BlogConfig(BaseModel):
    """Blog configuration"""
    homepage_heading: str
    homepage_subheading: str
    navbar_title: str
    about: str
    banner_image_url: str
