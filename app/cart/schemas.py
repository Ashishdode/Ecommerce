from pydantic import BaseModel

class CartAddRequest(BaseModel):
    product_id: int
    quantity: int

class CartUpdateRequest(BaseModel):
    quantity: int
