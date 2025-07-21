from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int
    API_PREFIX: str
    DEBUG: bool = False
    DATABASE_URL: str
    CELERY_BROKER: str
    GEMINI_API_KEY: str
    ELEVENLABS_API_KEY: str
    GEMINI_MODEL: str
    ELEVENLABS_MODEL: str
    BUCKET_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
