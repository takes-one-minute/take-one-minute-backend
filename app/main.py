from fastapi import FastAPI
from api import router as api_router
from db.session import SessionLocal, engine
from db.models import user_model, psych_model

import uvicorn

user_model.Base.metadata.create_all(bind=engine)
psych_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    # For Production Build
    # uvicorn.run("main:app", host="0.0.0.0", port=8000)

    # For Development Build
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)