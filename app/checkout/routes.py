from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.auth.utils import get_current_user
from app.cart.models import CartItem
from app.products.models import Product
from app.orders.models import Order, OrderItem

router = APIRouter(prefix="/checkout", tags=["Checkout"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def checkout(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order_items = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product: {product.name}"
            )
        
        product.stock -= item.quantity
        subtotal = product.price * item.quantity
        total += subtotal

        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase=product.price
        ))

    order = Order(user_id=user.id, total_amount=total, items=order_items)
    db.add(order)
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    db.refresh(order)
    return {"message": "Order placed successfully", "order_id": order.id}
