from pydantic import BaseSettings

class Settings(BaseSettings):
    telegram_token: str
    rabbitmq_url: str

    class Config:
        env_file = ".env"

settings = Settings()
