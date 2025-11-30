from enum import Enum

class Gender(str, Enum):
    M = 'M'
    F = 'F'

class ProductCategory(str, Enum):
    grain = 'grain'
    tuber = 'tuber'
    vegetable = 'vegetable'
    livestock = "livestock"
    diary = "diary"
    other = "other"

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"

class PaymentType(str, Enum):
    card = "card"
    transfer = "transfer"
    