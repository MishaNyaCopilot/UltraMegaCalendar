from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class UserConfig(Base):
    __tablename__ = "user_config"

    id = Column(Integer, primary_key=True, index=True)
    telegram_chat_id = Column(String, nullable=True)
    desktop_device_id = Column(String, nullable=True)
    default_reminder_minutes_before = Column(Integer, default=15)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user_config.id"))

    reminders = relationship("Reminder", back_populates="event")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    remind_at = Column(DateTime)
    notification_type = Column(String)
    is_sent = Column(Boolean, default=False)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="reminders")
