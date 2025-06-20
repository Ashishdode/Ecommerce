from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.cart import models, schemas
from app.auth.utils import get_current_user
from app.products.models import Product
from typing import List

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_to_cart(payload: schemas.CartAddRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=payload.product_id).first()
    desired_quantity = payload.quantity
    if item:
        desired_quantity += item.quantity
    
    if desired_quantity > product.stock:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    if item:
        item.quantity += payload.quantity
    else:
        item = models.CartItem(user_id=user.id, product_id=payload.product_id, quantity=payload.quantity)
        db.add(item)
    db.commit()
    return {"message": "Added to cart"}

@router.get("/")
def view_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user.id).all()
    return [{"product_id": item.product_id, "quantity": item.quantity} for item in cart_items]

@router.put("/{product_id}")
def update_cart(product_id: int, payload: schemas.CartUpdateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")

    if payload.quantity > product.stock:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    item.quantity = payload.quantity
    db.commit()
    return {"message": "Cart updated"}

@router.delete("/{product_id}")
def remove_from_cart(product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = db.query(models.CartItem).filter_by(user_id=user.id, product_id=product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}
