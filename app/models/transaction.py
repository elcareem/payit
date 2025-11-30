from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.types import Numeric
from sqlalchemy.sql import func
from .base import Base
from ..enums import PaymentType

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    payment_id = Column(Integer,  ForeignKey("payments.id", ondelete="CASCADE"), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
