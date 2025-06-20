from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.auth import models, schemas, utils
from app.core.database import SessionLocal, Base, engine
from sqlalchemy.exc import IntegrityError
from app.utils.email_utils import send_email
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=schemas.TokenResponse)
def signup(payload: schemas.SignupRequest, db: Session = Depends(get_db)):
    hashed_pw = utils.hash_password(payload.password)
    user = models.User(
        name=payload.name,
        email=payload.email,
        hashed_password=hashed_pw,
        role=payload.role
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        send_email(
            subject="Welcome to E-commerce!",
            recipient=user.email,
            body=f"Hi {user.name},\n\nThank you for signing up to our platform."
        )
    except Exception as e:
        print("Failed to send welcome email:", e)

    token = utils.create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token}

@router.post("/signin", response_model=schemas.TokenResponse)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = utils.create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token}

import uuid
from datetime import datetime, timedelta
from app.utils import email as email_utils
from app.auth.models import PasswordResetToken, User
from app.auth.schemas import ForgotPasswordRequest
from app.auth.schemas import ResetPasswordRequest

@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = str(uuid.uuid4())
    expiration = datetime.utcnow() + timedelta(minutes=15)

    reset_token = PasswordResetToken(user_id=user.id, token=token, expiration_time=expiration)
    db.add(reset_token)
    db.commit()

    email_utils.send_reset_email(user.email, token)
    return {"message": "Reset link sent to email"}

@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    reset_record = db.query(PasswordResetToken).filter_by(token=payload.token, used=False).first()
    if not reset_record or reset_record.is_expired():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter_by(id=reset_record.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = utils.hash_password(payload.new_password)
    reset_record.used = True
    db.commit()
    return {"message": "Password updated successfully"}
