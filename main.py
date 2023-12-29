from fastapi import FastAPI
from routers import auth, events



app = FastAPI()
app.include_router(auth.router)
app.include_router(events.router)


@app.get("/")
async def home():
    return {"hello ": "world2"}