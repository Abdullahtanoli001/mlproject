from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from src.api.database.database import SessionLocal
from src.api.models import User

SECRET_KEY = "your_secret_key_here"

user_router = APIRouter(prefix="/user")
auth_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.get("/profile")
def get_profile(token: str = Depends(auth_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    return {"username": user.username, "email": user.email}