from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import Numeric
from sqlalchemy.sql import func
from .base import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("product_categories.id", ondelete="CASCADE"), nullable = False)
    name = Column(String(50), min_length=3, max_length=50, nullable=False)
    description = Column(Text, nullable=True)
    unit_price = Column(Numeric(24, 12), nullable=False)
    quantity = Column(Integer, nullable=False)
    image_url = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
 
    farmer = relationship("Farmer", back_populates="products")
    orders = relationship("Order", back_populates="product")
    category = relationship("ProductCategory", back_populates="products")
