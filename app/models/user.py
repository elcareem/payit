from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
from app.enums import  Gender


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(11), unique=True, nullable = False) 
    email = Column(String(255), unique=True, index=True, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    location = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    farmer = relationship("Farmer", back_populates="user", uselist=False)
    buyer = relationship("Buyer", back_populates="user", uselist=False)