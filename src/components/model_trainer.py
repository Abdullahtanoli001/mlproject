# import dagshub
# dagshub.init(
#     repo_owner='Abdullahtanoli001',
#     repo_name='mlproject',
#     mlflow=True
# )

import mlflow
import mlflow.sklearn

import os
import sys
import numpy as np
from dataclasses import dataclass

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor
)
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_models, save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting train/test")

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoost": CatBoostRegressor(verbose=False),
                "AdaBoost": AdaBoostRegressor(),
            }

            params = {
                "Decision Tree": {
                    "criterion": ['squared_error', 'friedman_mse', 'absolute_error']
                },
                "Random Forest": {
                    "n_estimators": [8, 16, 32, 64, 128]
                },
                "Gradient Boosting": {
                    "learning_rate": [0.1, 0.01, 0.05],
                    "subsample": [0.7, 0.8, 0.9],
                    "n_estimators": [32, 64, 128]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    "learning_rate": [0.1, 0.01, 0.05],
                    "n_estimators": [32, 64, 128]
                },
                "CatBoost": {
                    "depth": [6, 8],
                    "learning_rate": [0.01, 0.05],
                    "iterations": [30, 50]
                },
                "AdaBoost": {
                    "learning_rate": [0.1, 0.01, 0.5],
                    "n_estimators": [32, 64, 128]
                }
            }

            # Evaluate all models
            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train,
                X_test=X_test, y_test=y_test,
                models=models, param=params
            )
            print("Model Report: ",model_report)
            # Best model + score
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]
            best_score = model_report[best_model_name]
            best_params = params.get(best_model_name, {})

            logging.info(f"BEST MODEL = {best_model_name}, Score = {best_score}")

            # Setup MLflow for DagsHub
            # mlflow.set_tracking_uri("https://dagshub.com/Abdullahtanoli001/mlproject.mlflow")

            # with mlflow.start_run():

            #     mlflow.log_param("best_model", best_model_name)
            #     mlflow.log_param("best_params", best_params)
            #     mlflow.log_metric("r2_score", best_score)

            #     # Avoid registry errors
            #     mlflow.set_registry_uri("file:///tmp/mlruns")

            #     mlflow.sklearn.log_model(
            #         sk_model=best_model,
            #         artifact_path="model"
            #     )

            # Save model locally
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            return best_score

        except Exception as e:
            raise CustomException(e, sys)
