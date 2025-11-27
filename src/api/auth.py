# src/api/auth.py
from passlib.context import CryptContext
from jose import jwt
import re
from datetime import datetime, timedelta


SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    password_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(password_bytes)

def verify_password(plain_password: str, hashed_password: str):
    plain_bytes = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(plain_bytes, hashed_password)

def create_access_token(data: dict, expires_minutes: int = 60) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validate_password(password: str) -> bool:
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
    return re.match(pattern, password) is not None
