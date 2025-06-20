from fastapi import FastAPI
from app.auth import routes as auth_routes
from app.core.database import engine
from app.auth import models as auth_models
from app.products import models as product_models, routes as product_routes
from app.products import public_routes as public_product_routes
from app.cart import models as cart_models, routes as cart_routes
from app.orders import models as order_models
from app.checkout import routes as checkout_routes
from app.orders import routes as order_routes


auth_models.Base.metadata.create_all(bind=engine)
product_models.Base.metadata.create_all(bind=engine)
cart_models.Base.metadata.create_all(bind=engine)
order_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(public_product_routes.router)
app.include_router(cart_routes.router)
app.include_router(checkout_routes.router)
app.include_router(order_routes.router)

from app.auth.models import PasswordResetToken
PasswordResetToken.__table__.create(bind=engine, checkfirst=True)
