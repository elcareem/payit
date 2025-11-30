from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.types import Numeric
from sqlalchemy.sql import func
from .base import Base
from ..enums import PaymentType

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    transaction_id = Column(Integer, unique=True, nullable=False)
    gateway = Column(String(50), nullable=False)
    type = Column(Enum(PaymentType), nullable=False)
    payload = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
