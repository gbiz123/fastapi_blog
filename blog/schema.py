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


class BlogConfig(BaseModel):
    """Blog configuration"""
    banner_image_url: str
    homepage_heading: str
    homepage_subheading: str


class Author(BaseModel):
    """Author"""

    name: str
    email: str
    bio: str
    organization: str | None
    linkedin_url: str | None
    twitter_url: str | None
    facebook_url: str | None
    instagram_url: str | None
    tumblr_url: str | None
