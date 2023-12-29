from fastapi import FastAPI
from routers import auth, events
from app import models
from app.database import engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(auth.router)
app.include_router(events.router)


@app.get("/")
async def home():
    return {"hello ": "world222222"}