from pydantic import BaseSettings

class Settings(BaseSettings):
    rabbitmq_url: str

    class Config:
        env_file = ".env"

settings = Settings()
