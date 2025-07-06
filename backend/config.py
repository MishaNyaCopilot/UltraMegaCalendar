from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str
    rabbitmq_url: str

    class Config:
        env_file = "backend/.env"

settings = Settings()
