from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.models import User
from src.api.auth import hash_password, verify_password, create_access_token, validate_password

def register_user(user, db: Session):
    if not validate_password(user.password):
        raise HTTPException(status_code=400, detail="Password must be strong")

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already used")

    hashed = hash_password(user.password)
    new_user = User(email=user.email, username=user.username, password=hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully!"}


def login_user(user, db: Session):
    if not user.username and not user.email:
        raise HTTPException(status_code=400, detail="Username or Email is required")

    db_user = None

    if user.username:
        db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user and user.email:
        db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username/email or password")

    token = create_access_token({"user_id": db_user.id})

    return {"access_token": token, "token_type": "bearer"}