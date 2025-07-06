from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.post("/users/{user_id}/events/", response_model=schemas.Event)
def create_event_for_user(
    user_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)
):
    return crud.create_event(db=db, event=event, user_id=user_id)


@app.get("/events/", response_model=list[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events
