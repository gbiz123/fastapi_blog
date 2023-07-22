from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row, text

import os

from . import models
from .. import schema


ENGINE = create_async_engine(os.environ["DATABASE_URL"])


async def get_db_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(ENGINE, expire_on_commit=False)


async def create_tables() -> None:
    async with ENGINE.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def fetch_user(
        async_session: async_sessionmaker[AsyncSession], 
        selector: int | str
    ) -> Row | None:
    """Fetch a user by ID or email.
    
    Args:
        selector (int | str): ID (int) or email (str) to select user by.
        async_session (AsyncSession): SQLAlchemy async session

    Returns:
        User
    """
    if isinstance(selector, int):
        stmt = text("SELECT * FROM users WHERE user_id = :selector")
    elif isinstance(selector, str):
        stmt = text("SELECT * FROM users WHERE email = :selector")
    else:
        raise TypeError("Must select user by id (int type) or by email (str type)")

    async with async_session() as session:
        params = {"selector": selector}
        result = await session.execute(stmt, params)
        return result.one_or_none()


async def fetch_post(
        async_session: async_sessionmaker[AsyncSession], 
        selector: int
    ) -> Row:
    """Fetch a post with author by post ID.
    
    Args:
        selector (int): ID to fetch a post by
        async_session (AsyncSession): SQLAlchemy async session

    Returns:
        Post
    """
    stmt = text(
        "SELECT * FROM posts WHERE post_id = :selector "
        "JOIN authors ON posts.author_id = authors.author_id"
    )
    async with async_session() as session:
        params = {"selector": selector}
        result = await session.execute(stmt, params)
        return result.one()


async def fetch_blog_config(async_session: async_sessionmaker[AsyncSession]) -> Row:
    """Fetch the blog's config table row
    
    Args:
        async_session (AsyncSession): SQLAlchemy async session

    Returns:
        BlogConfig
    """
    stmt = text("SELECT * FROM blog_config WHERE blog_config_id = 1")
    async with async_session() as session:
        result = await session.execute(stmt)
        return result.one()


async def fetch_posts(
        async_session: async_sessionmaker[AsyncSession], 
        limit: int,
        offset: int,
    ) -> list[Row]:
    """Fetch a post by ID.
    
    Args:
        selector (int): ID to fetch a post by
        async_session (AsyncSession): SQLAlchemy async session

    Returns:
        Post
    """
    stmt = text(
        "SELECT * FROM posts "
        "JOIN authors ON posts.author_id = authors.author_id "
        "ORDER BY date_created ASC "
        "LIMIT :limit "
        "OFFSET :offset"
    )
    async with async_session() as session:
        params = {"limit": limit, "offset": offset}
        results = await session.execute(stmt, params)
        return [result for result in results.all()] 


async def create_post(
        async_session: async_sessionmaker[AsyncSession],
        post: schema.Post
    ) -> None:
    """Create a new post
    
    Args:
        async_session (AsyncSession): SQLAlchemy async session
        post (schema.Post): Post for blog as defined in schema
    """
    stmt = text(
        "INSERT INTO posts "
        "    (title, content, author_id) "
        "VALUES "
        "   (:title, :content, :author_id)"
    )
    async with async_session() as session:
        async with session.begin():
            params = {
                "title": post.title,
                "content": post.content,
                "author_id": post.author_id
            }
            await session.execute(stmt, params)


async def create_user(
        async_session: async_sessionmaker[AsyncSession],
        user: schema.User
    ) -> None:
    """Create a new user
    
    Args:
        async_session (AsyncSession): SQLAlchemy async session
        user (schema.User): User for blog as defined in schema
    """
    stmt = text(
        "INSERT INTO users "
        "    (email, password, is_admin) "
        "VALUES "
        "   (:email, :password, :is_admin)"
    )
    async with async_session() as session:
        async with session.begin():
            params = {
                "email": user.email,
                "password": user.password,
                "is_admin": user.is_admin
            }
            await session.execute(stmt, params)


async def update_user(
        async_session: async_sessionmaker[AsyncSession],
        user_id: int,
        new_user: schema.User
    ) -> None:
    """Update a user
    
    Args:
        async_session (AsyncSession): SQLAlchemy async session
        new_user (schema.User): New data to update the user to
    """
    stmt = text(
        "UPDATE users SET"
        "    (email = :email, password = :password, is_admin = :is_admin) "
        "WHERE user_id = :user_id"
    )
    async with async_session() as session:
        async with session.begin():
            params = {
                "email": new_user.email,
                "password": new_user.password,
                "is_admin": new_user.is_admin,
                "user_id": user_id
            }
            await session.execute(stmt, params)


async def update_post(
        async_session: async_sessionmaker[AsyncSession],
        post_id: int,
        new_post: schema.Post
    ) -> None:
    """Create a new post
    
    Args:
        async_session (AsyncSession): SQLAlchemy async session
        post_id (int): ID of the post to update
        new_post (schema.Post): New post data
    """
    stmt = text(
        "UPDATE posts SET"
        "    (title = :title, content = :content, author_id = :author_id) "
        "WHERE post_id = :post_id"
    )
    async with async_session() as session:
        async with session.begin():
            params = {
                "title": new_post.title,
                "content": new_post.content,
                "author_id": new_post.author_id,
                "post_id": post_id
            }
            await session.execute(stmt, params)


async def update_blog_config(
        async_session: async_sessionmaker[AsyncSession],
        blog_config: schema.BlogConfig
    ) -> None:
    """Create a new post
    
    Args:
        async_session (AsyncSession): SQLAlchemy async session
        blog_config (BlogConfig): New configuration for the blog
    """
    stmt = text(
        "UPDATE blog_config SET"
        "    (banner_image_url = :banner_image_url, homepage_heading = :homepage_heading, homepage_subheading = :homepage_subheading) "
        "WHERE blog_config_id = 1"
    )
    async with async_session() as session:
        async with session.begin():
            params = {
                "banner_image_url": blog_config.banner_image_url,
                "homepage_heading": blog_config.homepage_heading,
                "homepage_subheading": blog_config.homepage_subheading,
            }
            await session.execute(stmt, params)


async def create_author(
        async_session: async_sessionmaker[AsyncSession],
        author: schema.Author
    ) -> None:
    """Create a new author
    
    Args:
        async_session (AsyncSession): SQLAlchemy async session
        author (schema.Author): Author for blog as defined in schema
    """
    stmt = text(
        "INSERT INTO authors ("
        "   name, "
        "   email, "
        "   organization, "
        "   bio, "
        "   linkedin_url, "
        "   twitter_url, "
        "   facebook_url, "
        "   instagram_url, "
        "   tumblr_url "
        ") "
        "VALUES ("
        "   :name, "
        "   :email, "
        "   :organization, "
        "   :bio, "
        "   :linkedin_url, "
        "   :twitter_url, "
        "   :facebook_url, "
        "   :instagram_url, "
        "   :tumblr_url "
        ") "
    )
    async with async_session() as session:
        async with session.begin():
            params =  {
                "name": author.name,
                "email": author.email,
                "organization": author.organization,
                "bio": author.bio,
                "linkedin_url": author.linkedin_url,
                "twitter_url": author.twitter_url,
                "facebook_url": author.facebook_url,
                "instagram_url": author.instagram_url,
                "tumblr_url": author.tumblr_url,
            }
            await session.execute(stmt, params)
