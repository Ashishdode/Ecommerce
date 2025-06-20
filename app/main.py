from fastapi import FastAPI
from app.auth import routes as auth_routes
from app.core.database import engine
from app.products import routes as product_routes
from app.products import public_routes as public_product_routes
from app.cart import routes as cart_routes
from app.checkout import routes as checkout_routes
from app.orders import routes as order_routes

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(public_product_routes.router)
app.include_router(cart_routes.router)
app.include_router(checkout_routes.router)
app.include_router(order_routes.router)
