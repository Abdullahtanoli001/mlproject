import sys
import pandas as pd

from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path='artifacts\model.pkl'
            preprocessor_path='artifacts\preprocessor.pkl'
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomException(e,sys)

class CustomData:
    def __init__(self,
        date: str,
        price: float,
        bedrooms: int,
        bathrooms: float,
        sqft_living: int,
        sqft_lot: int,
        floors: float,
        waterfront: int,
        view: int,
        condition: int,
        sqft_above: int,
        sqft_basement: int,
        yr_built: int,
        yr_renovated: int,
        street: str,
        city: str,
        statezip: str,
        country: str
    ):
        self.date = date
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.sqft_living = sqft_living
        self.sqft_lot = sqft_lot
        self.floors = floors
        self.waterfront = waterfront
        self.view = view
        self.condition = condition
        self.sqft_above = sqft_above
        self.sqft_basement = sqft_basement
        self.yr_built = yr_built
        self.yr_renovated = yr_renovated
        self.street = street
        self.city = city
        self.statezip = statezip
        self.country = country

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'date': [self.date],
                'price': [self.price],
                'bedrooms': [self.bedrooms],
                'bathrooms': [self.bathrooms],
                'sqft_living': [self.sqft_living],
                'sqft_lot': [self.sqft_lot],
                'floors': [self.floors],
                'waterfront': [self.waterfront],
                'view': [self.view],
                'condition': [self.condition],
                'sqft_above': [self.sqft_above],
                'sqft_basement': [self.sqft_basement],
                'yr_built': [self.yr_built],
                'yr_renovated': [self.yr_renovated],
                'street': [self.street],
                'city': [self.city],
                'statezip': [self.statezip],
                'country': [self.country]
            }

            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)
            