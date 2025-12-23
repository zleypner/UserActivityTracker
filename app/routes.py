from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Event
from app.schemas import EventCreate, EventResponse

router = APIRouter()


@router.post("/events", response_model=EventResponse, status_code=201)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(
        user_id=event.user_id,
        event_type=event.event_type,
        timestamp=event.timestamp or datetime.utcnow(),
        metadata=event.metadata
    )

    try:
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(e)}")


@router.get("/events", response_model=List[EventResponse])
def get_events(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    start_date: Optional[datetime] = Query(None, description="Filter events after this date"),
    end_date: Optional[datetime] = Query(None, description="Filter events before this date"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of events"),
    offset: int = Query(0, ge=0, description="Number of events to skip"),
    db: Session = Depends(get_db)
):
    query = db.query(Event)

    if user_id:
        query = query.filter(Event.user_id == user_id)

    if event_type:
        query = query.filter(Event.event_type == event_type)

    if start_date:
        query = query.filter(Event.timestamp >= start_date)

    if end_date:
        query = query.filter(Event.timestamp <= end_date)

    query = query.order_by(Event.timestamp.desc())

    events = query.offset(offset).limit(limit).all()

    return events


@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.get("/users/{user_id}/events", response_model=List[EventResponse])
def get_user_events(
    user_id: str,
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Event).filter(Event.user_id == user_id)

    if event_type:
        query = query.filter(Event.event_type == event_type)

    query = query.order_by(Event.timestamp.desc())

    events = query.offset(offset).limit(limit).all()

    return events
