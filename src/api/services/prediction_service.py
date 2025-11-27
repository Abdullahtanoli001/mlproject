from fastapi import HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from src.api.models import HousePricePrediction
from src.pipeline.predict_pipeline import predict_pipeline

SECRET_KEY = "your_secret_key_here"

def predict_house(data, token, db: Session):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    prediction = predict_pipeline(data.dict())

    new_record = HousePricePrediction(
        **data.dict(),
        prediction=float(prediction),
        user_id=user_id
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "message": "Prediction successful",
        "predicted_price": prediction
    }
