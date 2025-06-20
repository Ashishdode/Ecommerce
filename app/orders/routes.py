from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import SessionLocal
from app.auth.utils import get_current_user
from app.orders import models, schemas

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.OrderResponse])
def get_order_history(db: Session = Depends(get_db), user=Depends(get_current_user)):
    orders = db.query(models.Order).filter(models.Order.user_id == user.id).all()
    return orders

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order_details(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
