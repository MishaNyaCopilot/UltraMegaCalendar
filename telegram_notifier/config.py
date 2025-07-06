from pydantic import BaseSettings

class Settings(BaseSettings):
    telegram_token: str
    rabbitmq_url: str
    backend_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

settings = Settings()
