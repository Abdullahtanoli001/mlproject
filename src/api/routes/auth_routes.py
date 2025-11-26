from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.database.database import SessionLocal
from src.api.schemas.auth_schemas import RegisterSchema, LoginSchema
from src.api.services.auth_service import register_user, login_user

auth_router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/register")
def register(user: RegisterSchema, db: Session = Depends(get_db)):
    return register_user(user, db)

@auth_router.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    return login_user(user, db)
