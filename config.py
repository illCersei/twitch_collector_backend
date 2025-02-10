from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL_ASYNCPG: str
    DATABASE_URL_PSYCOPG2: str

    model_config = SettingsConfigDict(env_file="config.env", env_file_encoding="utf-8")

settings = Settings()
