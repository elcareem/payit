from pydantic import BaseModel, Field
from ..enums import OrderStatus
from decimal import Decimal

class Order(BaseModel):
    id: int
    product_id: int
    buyer_id: int
    unit_price: float
    quantity: int
    amount: float
    status: OrderStatus

class OrderCreateRequest(BaseModel):
    product_id: int
    quantity: int
    status: OrderStatus = OrderStatus.pending.value

class OrderUpdateRequest(BaseModel):
    quantity: int