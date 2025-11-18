from fastapi import FastAPI
from .database import engine
from .models.base import Base

from app.routes.user import router as user_router
import app.routes.product 

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

