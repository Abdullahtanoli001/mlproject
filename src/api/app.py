from fastapi import FastAPI
from src.api.database.database import Base, engine
from src.api.routes.auth_routes import auth_router
from src.api.routes.user_routes import user_router
from src.api.routes.prediction_routes import prediction_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(prediction_router)
