from fastapi import Request, Query, Form, Path
from fastapi.routing import APIRouter

from typing import Annotated

from starlette.responses import RedirectResponse

from ..schema import BlogConfig, Post, Author
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


@router.get("/create-post")
async def post_creator_page(request: Request):
    """Show the post creator page"""
    context = {"request": request}
    return templates.TemplateResponse("create_post.html", context)


@router.post("/create-post")
async def create_post(
        request: Request,
        author_id: int = Form(gt=0, lt=10e6), 
        content: str = Form(),
        title: str = Form()
    ):
    """Create a new post"""
    post = Post(author_id=author_id, content=content, title=title)
    sessionmaker = await db.get_db_sessionmaker()
    await db.create_post(sessionmaker, post)
    request.session["message"] = "New post created!"    
    return RedirectResponse("/", status_code=303)


@router.get("/create-author")
async def author_creator_page(request: Request):
    """Show the author creator page"""
    context = {"request": request}
    return templates.TemplateResponse("create_author.html", context)


@router.post("/create-author")
async def create_author(
        request: Request,
        name: str = Form(""),
        email: str = Form(""),
        bio: str = Form(""),
        organization: str | None = Form(None),
        linkedin_url: str | None = Form(None),
        twitter_url: str | None = Form(None),
        facebook_url: str | None = Form(None),
        instagram_url: str | None = Form(None),
        tumblr_url: str | None = Form(None)
    ):
    """Create a new author"""
    if not all([name, email, bio]):
        request.session["message"] = "Name, email, and bio are required." 
        return RedirectResponse("/create-author", status_code=303)

    author = Author(
        name=name,
        email=email,
        organization=organization,
        bio=bio,
        linkedin_url=linkedin_url,
        twitter_url=twitter_url,
        facebook_url=facebook_url,
        instagram_url=instagram_url,
        tumblr_url=tumblr_url,
    )
    sessionmaker = await db.get_db_sessionmaker()
    await db.create_author(sessionmaker, author)
    request.session["message"] = f"Author {name} created!" 
    return RedirectResponse("/", status_code=303)


@router.get("/update-post/{post_no}")
async def post_editor_page(request: Request, post_no: Annotated[int, Path(gt=0, lt=10e6)]):
    """Show the post editor page"""
    sessionmaker = await db.get_db_sessionmaker()
    post = await db.fetch_post(sessionmaker, post_no)
    context = {
        "request": request,
        "post": post
    }
    return templates.TemplateResponse("edit_post.html", context)


@router.post("/update-post")
async def update_post(
        post_id: Annotated[int, Query(gt=0, lt=10e6)],
        author_id: int = Form(gt=0, lt=10e6), 
        content: str = Form(),
        title: str = Form()
    ):
    """Update a post"""
    post = Post(author_id=author_id, content=content, title=title)
    sessionmaker = await db.get_db_sessionmaker()
    await db.update_post(sessionmaker, post_id, post)


@router.get("/update-blog-config")
async def show_config_editor_page(request: Request):
    """Update the blog config"""
    context = {"request": request}
    return templates.TemplateResponse("edit_config.html", context)


@router.post("/update-blog-config")
async def update_blog_config(
        homepage_heading: str = Form(),
        homepage_subheading: str = Form(),
        banner_image_url: str = Form()
    ):
    """Update the blog config"""
    blog_config = BlogConfig(banner_image_url=banner_image_url,
                             homepage_subheading=homepage_subheading,
                             homepage_heading=homepage_heading)
    
    sessionmaker = await db.get_db_sessionmaker()
    await db.update_blog_config(sessionmaker, blog_config)

