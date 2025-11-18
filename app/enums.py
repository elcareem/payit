from sqlalchemy import Enum
from enum import Enum as _Enum

class GenderBase(str, Enum):
    M = 'M'
    F = 'F'

class CategoryBase(str, Enum):
    buyer = 'buyer'
    farmer = 'farmer'

class Gender(str, _Enum):
    M = 'M'
    F = 'F'

class Category(str, _Enum):
    buyer = 'buyer'
    farmer = 'farmer'