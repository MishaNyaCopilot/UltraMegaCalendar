from pydantic import BaseModel
from datetime import datetime

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
    reminders: list[Reminder] = []

    class Config:
        orm_mode = True

class UserConfigBase(BaseModel):
    telegram_chat_id: str | None = None
    desktop_device_id: str | None = None

class UserConfigCreate(UserConfigBase):
    pass

class UserConfig(UserConfigBase):
    id: int

    class Config:
        orm_mode = True
