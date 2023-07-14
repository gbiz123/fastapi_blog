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
    organization: str
    bio: str
    linkedin_url: str
    twitter_url: str
    facebook_url: str
    instagram_url: str
    tumblr_url: str
