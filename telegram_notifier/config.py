from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    telegram_token: str
    rabbitmq_url: str
    backend_url: str = "http://localhost:8000"

    class Config:
        env_file = "telegram_notifier/.env"

settings = Settings()
