from fastapi import FastAPI
from .database import engine
from .models.base import Base
from .models import product_category, product_image
from fastapi.staticfiles import StaticFiles
from app.admin import init_admin
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routes.user_route import router as user_router
from app.routes.product_route import router as product_router
from app.routes.auth_route import router as auth_router
from app.routes.order_route import router as order_router
from app.routes.oauth_route import router as oauth_router

import os

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(oauth_router)


app.mount("/static", StaticFiles(directory="static"), name="static")

init_admin(app, engine)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("JWT_SECRET_KEY"),
    https_only=False
)

origins = {
    "http://localhost:8000"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)