from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.types import Numeric
from sqlalchemy.sql import func
from .base import Base
from pydantic import BaseModel

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(Numeric(12, 12), nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(Enum('grains', 'tuber', 'vegetables'), nullable = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

 
    