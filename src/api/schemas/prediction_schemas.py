from pydantic import BaseModel

class HouseInput(BaseModel):
    bedrooms: float
    bathrooms: float
    sqft_living: float
    sqft_lot: float
    floors: float
    waterfront: int = 0
    view: int = 0
    condition: int
    sqft_above: float
    sqft_basement: float
    yr_built: int
    yr_renovated: int
    street: str = "Unknown"
    city: str
    statezip: str = "00000"
    country: str = "USA"
