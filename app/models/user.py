from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from .base import Base
from pydantic import BaseModel, EmailStr
from app.enums import  Gender, Category



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(11), nullable = False)
    email = Column(String(255), index=True, unique=True, nullable=False)
    gender = Column(Enum('M', 'F'), nullable=False)
    category = Column(Enum('buyer', 'farmer'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class UserCreate(BaseModel):
    username: str
    password: str
    phone: str
    email: EmailStr
    gender: Gender 
    category: Category

class UserResponse(BaseModel):
    id: int
    username: str
    phone: str
    email: EmailStr
    gender: Gender
    category: Category

