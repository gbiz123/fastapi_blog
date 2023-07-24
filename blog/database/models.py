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
    is_author: Mapped[bool]
    name: Mapped[str]
    bio: Mapped[str]
    organization: Mapped[str]
    social_media_link: Mapped[str]


class Post(Base):
    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    date_created: Mapped[DateTime] = mapped_column(DateTime, server_default=now())
    title: Mapped[str]
    description: Mapped[str]
    content: Mapped[str]
    created_by_user_id: Mapped[str]
    image_url: Mapped[str] = mapped_column(String, nullable=True)


class BlogConfig(Base):
    __tablename__ = "blog_config"

    blog_config_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    navbar_title: Mapped[str]
    homepage_heading: Mapped[str]
    homepage_subheading: Mapped[str]
    banner_image_url: Mapped[str]
    about: Mapped[str]
