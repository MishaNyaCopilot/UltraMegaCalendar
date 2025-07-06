from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from . import models, schemas
from .broker import broker


def get_user_config(db: Session, user_id: int):
    return db.query(models.UserConfig).filter(models.UserConfig.id == user_id).first()


def create_user_config(db: Session, user: schemas.UserConfigCreate):
    db_user = models.UserConfig(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_config(db: Session, user_id: int, user: schemas.UserConfigCreate):
    db_user = db.query(models.UserConfig).filter(models.UserConfig.id == user_id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user_config(db: Session, user_id: int):
    db_user = db.query(models.UserConfig).filter(models.UserConfig.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


async def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    db_event = models.Event(**event.dict(), user_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Calculate reminder time (e.g., 5 minutes before the event)
    remind_at = event.start_time - timedelta(minutes=5)
    delay_ms = int((remind_at - datetime.now()).total_seconds() * 1000)

    # Get user config to send notifications
    user_config = get_user_config(db, user_id)

    if user_config:
        if user_config.telegram_chat_id:
            await broker.publish(
                {
                    "type": "reminder",
                    "event_id": db_event.id,
                    "event_title": db_event.title,
                    "remind_at": remind_at.isoformat(),
                    "target_type": "telegram",
                    "telegram_chat_id": user_config.telegram_chat_id,
                },
                "notification.telegram",
                delay=delay_ms
            )
        if user_config.desktop_device_id:
            await broker.publish(
                {
                    "type": "reminder",
                    "event_id": db_event.id,
                    "event_title": db_event.title,
                    "remind_at": remind_at.isoformat(),
                    "target_type": "desktop",
                    "desktop_device_id": user_config.desktop_device_id,
                },
                "notification.desktop",
                delay=delay_ms
            )

    return db_event

def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        for key, value in event.dict(exclude_unset=True).items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event
