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


@router.get("/logout")
async def logout_user(request: Request):
    if not request.session.get("user"):
        request.session["message"] = "You are not logged in."
        return RedirectResponse("/", 303)

    request.session.pop("user")
    request.session["message"] = "You have been logged out."
    return RedirectResponse("/", 303)


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
    
    request.session["user"] = db.row_to_dict(user)
    request.session["message"] = "Welcome to your blog!"
    return RedirectResponse("/", 303)
