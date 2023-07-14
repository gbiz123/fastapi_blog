from fastapi import Query, Request
from fastapi.routing import APIRouter

from typing import Annotated

from ..schema import BlogConfig, Post
from ..templates import templates
from .. import database as db


router = APIRouter(prefix="/admin")


@router.post("/create-post")
async def create_post(post: Post):
    """Create a new post"""
    sessionmaker = await db.get_db_sessionmaker()
    await db.create_post(sessionmaker, post)


@router.post("/update-post")
async def update_post(post_id: Annotated[int, Query(gt=0, lt=10e6)], new_post: Post):
    """Update a post"""
    sessionmaker = await db.get_db_sessionmaker()
    await db.update_post(sessionmaker, post_id, post)


