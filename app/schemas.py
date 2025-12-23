from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class EventCreate(BaseModel):
    user_id: str = Field(..., min_length=1, description="User identifier")
    event_type: str = Field(..., min_length=1, description="Type of event (e.g., login, page_view, click, logout)")
    timestamp: Optional[datetime] = Field(None, description="Event timestamp (defaults to current time)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional event data as JSON")


class EventResponse(BaseModel):
    id: int
    user_id: str
    event_type: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class EventQueryParams(BaseModel):
    user_id: Optional[str] = None
    event_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(100, ge=1, le=1000, description="Maximum number of events to return")
    offset: int = Field(0, ge=0, description="Number of events to skip")
