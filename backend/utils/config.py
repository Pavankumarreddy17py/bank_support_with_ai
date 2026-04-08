from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Bank Support AI"
    environment: str = "dev"
    db_url: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"

settings = Settings()
