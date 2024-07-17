from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


class AppConfig(Config):
    secret_key: str
    BASE_DIR: Path = Path()
    template_folder: Path = BASE_DIR / "static/templates/"


class Settings(BaseSettings):
    app: AppConfig = AppConfig()


settings = Settings()
