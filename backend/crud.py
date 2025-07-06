from sqlalchemy.orm import Session

from . import models, schemas


def get_user_config(db: Session, user_id: int):
    return db.query(models.UserConfig).filter(models.UserConfig.id == user_id).first()


def create_user_config(db: Session, user: schemas.UserConfigCreate):
    db_user = models.UserConfig(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    db_event = models.Event(**event.dict(), user_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
