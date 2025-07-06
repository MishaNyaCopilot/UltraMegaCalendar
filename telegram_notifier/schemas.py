from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime | None = None
    location: str | None = None
    is_completed: bool = False

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class ReminderBase(BaseModel):
    remind_at: datetime
    notification_type: str

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    is_sent: bool
    event_id: int

    class Config:
        orm_mode = True
