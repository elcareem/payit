from sqlalchemy import Column, Integer, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
from ..enums import ProductCategory


class ProductCategory(Base):
    __tablename__ = "product_categories" 
    id = Column(Integer, primary_key=True)
    name = Column(Enum(ProductCategory), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    products = relationship("Product", back_populates="category")

