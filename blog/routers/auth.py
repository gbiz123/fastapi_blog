"""Password authentication flows"""

from fastapi import Form, Request
from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse

from ..templates import templates
from .. import database as db
from .. import schema

import bcrypt

import os
import re

import blog

router = APIRouter(prefix="/auth")


@router.get("/login")
async def login_page(request: Request):
    """Show the login page"""
    sessionmaker = await db.get_db_sessionmaker()
    blog_config = await db.fetch_blog_config(sessionmaker)
    return templates.TemplateResponse("login.html", 
                                      {"request": request,
                                       "blog_config": blog_config})


@router.post("/login")
async def login_user(
        request: Request,
        email: str = Form(""),
        password: str = Form(""),
    ):
    """Show the login page"""
    if not email or not password:
        request.session["message"] = "Please enter your username or password before proceeding."
        return RedirectResponse("/auth/login", 303)

    sessionmaker = await db.get_db_sessionmaker()
    user = await db.fetch_user(sessionmaker, email)
    
    if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
        request.session["message"] = "Invalid email or password."
        return RedirectResponse("/auth/login", 303)

    request.session["message"] = "Welcome to your blog!"
    return RedirectResponse("/", 303)


@router.get("/create-user")
async def create_user_page(request: Request):
    """Show the create_user page"""
    return templates.TemplateResponse("create_user.html", {"request": request})


@router.post("/create-user")
async def create_user(
        request: Request,
        email: str = Form(""),
        password: str = Form(""),
        is_admin: str = Form("off"),
        is_author: str = Form("off")
    ):
    """Create a new user"""
    if not request.session.get("user").get("is_admin"):
        request.session["message"] = "You must be logged in as an admin to create users."
        return RedirectResponse("/", 303)

    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = schema.User(
        email=email,
        password=password,
        is_admin=True if is_admin == "on" else False,
        is_author=True if is_author == "on" else False
    )
    sessionmaker = await db.get_db_sessionmaker()
    await db.create_user(sessionmaker, user)
    request.session["message"] = "New user created"
    return RedirectResponse("/", 303)
