from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List

class Product(BaseModel):
    id: int
    farmer_id: int
    category_id: int
    name: str
    unit_price: float
    quantity: int

    model_config = {
        "from_attributes": True
    }

class ProductDetail(BaseModel):
    id: int
    farmer_id: int
    category_id: int
    name: str
    unit_price: float
    quantity: int
    image_urls: List[str]
    


class ProductCreateRequest(BaseModel):
    category_id: int
    name: str = Field(min_length=3, max_length=50)
    unit_price: Decimal = Field(max_digits=24, decimal_places=12) 
    quantity: int = Field(ge=0, le=1000) 

class ProductUpdateRequest(BaseModel):
    category_id: int = None
    name: str = Field(None, min_length=3, max_length=50)
    unit_price: Decimal = Field(None, max_digits=24, decimal_places=12) 
    quantity: int = Field(None, ge=0, le=1000) 




