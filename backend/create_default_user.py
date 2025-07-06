from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import crud, schemas, models

models.Base.metadata.create_all(bind=engine)

def create_default_user():
    db = SessionLocal()
    try:
        user = crud.get_user_config(db, user_id=1)
        if not user:
            print("Creating default user with ID 1...")
            user_in = schemas.UserConfigCreate(
                telegram_chat_id=None,
                desktop_device_id=None,
                default_reminder_minutes_before=15
            )
            crud.create_user_config(db=db, user=user_in)
            print("Default user created.")
        else:
            print("Default user with ID 1 already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_user()
