from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import crud, schemas, models

models.Base.metadata.create_all(bind=engine)

def update_default_user_desktop_device_id(device_id: str):
    db = SessionLocal()
    try:
        user = crud.get_user_config(db, user_id=1)
        if user:
            print(f"Updating desktop_device_id for user ID 1 to {device_id}...")
            user_in = schemas.UserConfigCreate(
                telegram_chat_id=user.telegram_chat_id,
                desktop_device_id=device_id,
                default_reminder_minutes_before=user.default_reminder_minutes_before
            )
            crud.update_user_config(db=db, user_id=1, user=user_in)
            print("Desktop device ID updated.")
        else:
            print("Default user with ID 1 not found.")
    finally:
        db.close()

if __name__ == "__main__":
    update_default_user_desktop_device_id("default-desktop-device")
