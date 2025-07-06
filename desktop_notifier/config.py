from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    rabbitmq_url: str

    class Config:
        env_file = "desktop_notifier/.env"

settings = Settings()
