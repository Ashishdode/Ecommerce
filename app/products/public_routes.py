from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import SessionLocal
from app.products import models, schemas

router = APIRouter(prefix="/products", tags=["Public Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query(None, description="Options: price, name"),
    page: int = 1,
    page_size: int = 10,
):
    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category == category)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    if sort_by == "price":
        query = query.order_by(models.Product.price)
    elif sort_by == "name":
        query = query.order_by(models.Product.name)

    products = query.offset((page - 1) * page_size).limit(page_size).all()
    return products

@router.get("/search", response_model=List[schemas.ProductResponse])
def search_products(keyword: str, db: Session = Depends(get_db)):
    return db.query(models.Product).filter(models.Product.name.ilike(f"%{keyword}%")).all()

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
