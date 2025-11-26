from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from src.api.database.database import SessionLocal
from src.api.schemas.prediction_schemas import HouseInput
from src.api.services.prediction_service import predict_house

prediction_router = APIRouter(prefix="/predict")
auth_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@prediction_router.post("/")
def predict(data: HouseInput, token=Depends(auth_scheme), db: Session = Depends(get_db)):
    return predict_house(data, token, db)
