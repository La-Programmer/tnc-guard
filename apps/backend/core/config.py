from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_URI: str

    class Config:
        env_file = ".env"

settings = Settings()
