from fastapi import Query, Request, Form, Path
from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse

import bcrypt

from typing import Annotated

from .. import schema
from ..schema import BlogConfig, Post
from ..templates import templates
from .. import database as db


router = APIRouter(prefix="/admin")


@router.get("/create-post")
async def post_creator_page(request: Request):
    """Show the post creator page"""
    sessionmaker = await db.get_db_sessionmaker()
    blog_config = await db.fetch_blog_config(sessionmaker)
    context = {"request": request, "blog_config": blog_config}
    return templates.TemplateResponse("create_post.html", context)


@router.post("/create-post")
async def create_post(
        request: Request,
        content: str = Form(""),
        description: str = Form(""),
        image_url: str = Form(""),
        title: str = Form("")
    ):
    """Create a new post"""
    user = request.session.get("user")
    if not user:
        request.session["message"] = "You need to login to make a post."    
        return RedirectResponse("/auth/login", status_code=303)

    if not all([image_url, content, title, description]):
        request.session["message"] = "Title, image URL, description, and content are required."    
        return RedirectResponse("/create-post", status_code=303)

    user_id = user["user_id"]

    post = Post(user_id=user_id,
                image_url=image_url,
                content=content,
                title=title,
                description=description)
    sessionmaker = await db.get_db_sessionmaker()
    await db.create_post(sessionmaker, post)
    request.session["message"] = "New post created!"    
    return RedirectResponse("/", status_code=303)


@router.get("/update-post/{post_id}")
async def update_post_page(request: Request, post_id: Annotated[int, Path(gt=0, lt=10e6)]):
    """Show the post editor page"""
    sessionmaker = await db.get_db_sessionmaker()
    post = await db.fetch_post(sessionmaker, post_id)
    blog_config = await db.fetch_blog_config(sessionmaker)
    context = {
        "request": request,
        "post": post,
        "blog_config": blog_config
    }
    return templates.TemplateResponse("update_post.html", context)


@router.post("/update-post")
async def update_post(
        request: Request,
        post_id: Annotated[int, Query(gt=0, lt=10e6)],
        content: str = Form(""),
        description: str = Form(""),
        title: str = Form(""),
        image_url: str = Form("")
    ):
    """Update a post"""
    user = request.session.get("user")
    if not user:
        request.session["message"] = "You need to login to make a post."    
        return RedirectResponse("/auth/login", status_code=303)

    if not all([image_url, content, title, description]):
        request.session["message"] = "Title, image URL, description, and content are required."    
        return RedirectResponse("/create-post", status_code=303)

    user_id = user["user_id"]

    post = Post(user_id=user_id,
                image_url=image_url,
                content=content,
                title=title,
                description=description)

    sessionmaker = await db.get_db_sessionmaker()
    await db.update_post(sessionmaker, post_id, post)
    request.session["message"] = "Post updated!"    
    return RedirectResponse("/", status_code=303)


@router.get("/update-blog-config")
async def update_config_page(request: Request):
    """Update the blog config"""
    if not request.session.get("user"):
        request.session["message"] = "You must be logged in as an admin to update config."
        return RedirectResponse("/", 303)

    if not request.session["user"]["is_admin"]:
        request.session["message"] = "You must be logged in as an admin to update config."
        return RedirectResponse("/", 303)

    sessionmaker = await db.get_db_sessionmaker()
    blog_config = await db.fetch_blog_config(sessionmaker)
    context = {"request": request, "blog_config": blog_config}
    return templates.TemplateResponse("update_config.html", context)


@router.post("/update-blog-config")
async def update_blog_config(
        request: Request,
        homepage_heading: str = Form(""),
        homepage_subheading: str = Form(""),
        banner_image_url: str = Form(""),
        about: str = Form(""),
        navbar_title: str = Form("")
    ):
    """Update the blog config"""
    if not request.session.get("user"):
        request.session["message"] = "You must be logged in as an admin to update config."
        return RedirectResponse("/", 303)

    if not request.session["user"]["is_admin"]:
        request.session["message"] = "You must be logged in as an admin to update config."
        return RedirectResponse("/", 303)

    if not all([homepage_subheading, homepage_subheading, navbar_title, about, banner_image_url]):
        request.session["message"] = "Please fill in all the required fields."    
        return RedirectResponse("/admin/update-blog-config", status_code=303)

    blog_config = BlogConfig(banner_image_url=banner_image_url,
                             homepage_subheading=homepage_subheading,
                             homepage_heading=homepage_heading,
                             about=about,
                             navbar_title=navbar_title)
    
    sessionmaker = await db.get_db_sessionmaker()
    await db.update_blog_config(sessionmaker, blog_config)
    request.session["message"] = "Your blog config has been updated!"    
    return RedirectResponse("/", status_code=303)


@router.get("/create-user")
async def create_user_page(request: Request):
    """Show the create_user page"""
    if not request.session.get("user"):
        request.session["message"] = "You must be logged in as an admin to create users."
        return RedirectResponse("/", 303)

    if not request.session["user"]["is_admin"]:
        request.session["message"] = "You must be logged in as an admin to create users."
        return RedirectResponse("/", 303)

    sessionmaker = await db.get_db_sessionmaker()
    blog_config = await db.fetch_blog_config(sessionmaker)
    context = {"request": request, "blog_config": blog_config}
    return templates.TemplateResponse("create_user.html", context)


@router.post("/create-user")
async def create_user(
        request: Request,
        email: str = Form(""),
        name: str = Form(""),
        bio: str = Form(""),
        password: str = Form(""),
        is_admin: str = Form("off"),
    ):
    """Create a new user"""
    if not request.session.get("user"):
        request.session["message"] = "You must be logged in as an admin to create users."
        return RedirectResponse("/", 303)

    if not request.session["user"]["is_admin"]:
        request.session["message"] = "You must be logged in as an admin to create users."
        return RedirectResponse("/", 303)

    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = schema.User(
        email=email,
        password=password,
        name=name,
        bio=bio,
        is_admin=True if is_admin == "on" else False,
    )
    sessionmaker = await db.get_db_sessionmaker()

    if await db.fetch_user(sessionmaker, email):
        request.session["message"] = "That email is taken."
        return RedirectResponse("/auth/create-user", 303)

    await db.create_user(sessionmaker, user)
    request.session["message"] = "New user created"
    return RedirectResponse("/", 303)
