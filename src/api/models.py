# src/api/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.api.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(String, default=datetime.utcnow().isoformat())

    # Relationship: User -> HousePricePrediction
    predictions = relationship("HousePricePrediction", back_populates="user")


class HousePricePrediction(Base):
    __tablename__ = "house_price_predictions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, default=datetime.utcnow().isoformat())
    bedrooms = Column(Float)
    bathrooms = Column(Float)
    sqft_living = Column(Float)
    sqft_lot = Column(Float)
    floors = Column(Float)
    waterfront = Column(Integer, default=0)
    view = Column(Integer, default=0)
    condition = Column(Integer)
    sqft_above = Column(Float)
    sqft_basement = Column(Float)
    yr_built = Column(Integer)
    yr_renovated = Column(Integer)
    street = Column(String, default="Unknown")
    city = Column(String)
    statezip = Column(String, default="00000")
    country = Column(String, default="USA")
    prediction = Column(Float)
    created_at = Column(String, default=datetime.utcnow().isoformat())

    # Link to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="predictions")
