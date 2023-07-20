from sqlalchemy import Integer, String, DateTime, Identity, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import now


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=now())
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool]


class Post(Base):
    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=now())
    title: Mapped[str]
    content: Mapped[str]
    author_id: Mapped[str] = mapped_column(Integer, ForeignKey("authors.author_id"))


class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    bio: Mapped[str]
    organization: Mapped[str] = mapped_column(String)
    linkedin_url: Mapped[str] = mapped_column(String)
    twitter_url: Mapped[str] = mapped_column(String)
    facebook_url: Mapped[str] = mapped_column(String)
    instagram_url: Mapped[str] = mapped_column(String)
    tumblr_url: Mapped[str] = mapped_column(String)


class BlogConfig(Base):
    __tablename__ = "blog_config"

    blog_config_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    homepage_heading: Mapped[str]
    homepage_subheading: Mapped[str]
    banner_image_url: Mapped[str]
