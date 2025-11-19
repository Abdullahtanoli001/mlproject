from fastapi import FastAPI
from pydantic import BaseModel
from typing import Annotated
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = FastAPI()

class UserInput(BaseModel):
    bedrooms: float
    bathrooms: float
    sqft_living: int
    sqft_lot: int
    floors: float
    condition: int
    city: str


@app.post("/predict")
def predict_price(data: UserInput):

    # ---- create object of CustomData with missing default values ----
    custom_data = CustomData(
        date="2025-01-01",
        price=0,
        bedrooms=data.bedrooms,
        bathrooms=data.bathrooms,
        sqft_living=data.sqft_living,
        sqft_lot=data.sqft_lot,
        floors=data.floors,
        waterfront=0,
        view=0,
        condition=data.condition,
        sqft_above=data.sqft_living,     # temporary
        sqft_basement=0,
        yr_built=2000,
        yr_renovated=0,
        street="Unknown",
        city=data.city,
        statezip="00000",
        country="USA"
    )

    final_df = custom_data.get_data_as_dataframe()

    pipeline = PredictPipeline()
    prediction = pipeline.predict(final_df)[0]

    return {"predicted_price": prediction}
