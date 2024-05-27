from fastapi import FastAPI
from app.api import router as api_router
from app.db.session import SessionLocal, engine
from app.db.models import user_model, psych_model

user_model.Base.metadata.create_all(bind=engine)
psych_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)