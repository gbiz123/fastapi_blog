from fastapi import Request, Query, Form, Path
from fastapi.routing import APIRouter

from typing import Annotated

from starlette.responses import RedirectResponse

from ..schema import BlogConfig, Post
from ..templates import templates
from .. import database as db


router = APIRouter(prefix="")


@router.get("/")
async def homepage(request: Request):
    sessionmaker = await db.get_db_sessionmaker()
    posts = await db.fetch_posts(sessionmaker, 10, 0)
    blog_config = await db.fetch_blog_config(sessionmaker)

    context = {
        "request": request,
        "posts": posts,
        "blog_config": blog_config
    }
    
    return templates.TemplateResponse("home.html", context)


@router.get("/page/{page_no}")
async def homepage(request: Request, page_no: Annotated[int, Path(gt=0, lt=10e6)] ):
    if page_no == 1:
        return RedirectResponse("/", 303)

    sessionmaker = await db.get_db_sessionmaker()
    limit = (page_no - 1) * 10 + 10
    offset = (page_no - 1) * 10
    posts = await db.fetch_posts(sessionmaker, limit, offset) 
    blog_config = await db.fetch_blog_config(sessionmaker)

    context = {
        "request": request,
        "posts": posts,
        "blog_config": blog_config
    }
    
    return templates.TemplateResponse("home.html", context)



@router.get("/post/{post_no}")
async def blog_post_page(
        request: Request,
        post_no: Annotated[int, Path(gt=0, lt=10e6)]
    ):
    """Load a blog post page by post number"""
    sessionmaker = await db.get_db_sessionmaker()
    blog_config = await db.fetch_blog_config(sessionmaker)
    post = await db.fetch_post(sessionmaker, post_no)
    if not post:
        request.session["message"] = "Could not find that post."    
        return RedirectResponse("/", status_code=303)

    context = {"request": request, "blog_config": blog_config, "post": post}
    return templates.TemplateResponse("blog_post.html", context)
