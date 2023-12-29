from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.oauth2 import get_current_user
from app import models ,schema
from app.database import connect_db
from datetime import datetime

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("/")
async def get_events():
    return {"test": "events"}



@router.post("/events", status_code=status.HTTP_201_CREATED)
def create_event(event: schema.Event, db: Session = Depends(connect_db), current_user: int = Depends(get_current_user)):
    parsed_time = datetime.strptime(event.time, "%H:%M:%S").time()
    event.time = parsed_time
    print(parsed_time)
    if current_user is not None:
        event.owner_id = current_user.id
        new_event = models.Event(**event.model_dump())
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return  new_event
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please login in ")