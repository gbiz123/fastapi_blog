from fastapi import FastAPI

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

import os

from dotenv import load_dotenv
load_dotenv()

def app():

    middleware = [
        Middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"]),
        Middleware(GZipMiddleware)
    ]

    routes = [
        Mount('/static', app=StaticFiles(directory='./blog/static'), name='static'),
    ]

    app = FastAPI(middleware=middleware, routes=routes)

    from .routers import home
    app.include_router(home.router)

    from .routers import auth
    app.include_router(auth.router)

    from .routers import admin
    app.include_router(admin.router)

    return app
