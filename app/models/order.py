from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.types import Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
from ..enums import OrderStatus

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("buyers.id", ondelete="CASCADE"), nullable=False)
    unit_price = Column(Numeric(24, 12), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Numeric, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

 
    product = relationship("Product", back_populates="orders")
    buyer = relationship("Buyer", back_populates="orders")