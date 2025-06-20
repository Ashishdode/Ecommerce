from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: Optional[str] = None
    image_url: Optional[str] = None

class ProductUpdate(ProductCreate):
    pass

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True
