from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .broker import broker

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    yield
    await broker.close()

app = FastAPI(lifespan=lifespan)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserConfig)
def create_user(user: schemas.UserConfigCreate, db: Session = Depends(get_db)):
    return crud.create_user_config(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.UserConfig)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_config(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.UserConfig)
def update_user(user_id: int, user: schemas.UserConfigCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user_config(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=schemas.UserConfig)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user_config(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/events/", response_model=schemas.Event)
async def create_event_for_user(
    user_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)
):
    db_event = await crud.create_event(db=db, event=event, user_id=user_id)
    return db_event


@app.get("/events/", response_model=list[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@app.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.put("/events/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = crud.update_event(db, event_id, event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.delete("/events/{event_id}", response_model=schemas.Event)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.delete_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.post("/events/{event_id}/reminders/", response_model=schemas.Reminder)
def create_reminder_for_event(
    event_id: int, reminder: schemas.ReminderCreate, db: Session = Depends(get_db)
):
    return crud.create_reminder(db=db, reminder=reminder, event_id=event_id)


@app.get("/reminders/", response_model=list[schemas.Reminder])
def read_reminders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reminders = crud.get_reminders(db, skip=skip, limit=limit)
    return reminders


@app.get("/reminders/{reminder_id}", response_model=schemas.Reminder)
def read_reminder(reminder_id: int, db: Session = Depends(get_db)):
    db_reminder = crud.get_reminder(db, reminder_id=reminder_id)
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return db_reminder


@app.put("/reminders/{reminder_id}", response_model=schemas.Reminder)
def update_reminder(reminder_id: int, reminder: schemas.ReminderCreate, db: Session = Depends(get_db)):
    db_reminder = crud.update_reminder(db, reminder_id, reminder)
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return db_reminder


@app.delete("/reminders/{reminder_id}", response_model=schemas.Reminder)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    db_reminder = crud.delete_reminder(db, reminder_id)
    if db_reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return db_reminder