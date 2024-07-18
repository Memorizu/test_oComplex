from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from flask_caching import Cache


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


class RedisConfig(Config):

    host: str
    port: int

    @property
    def url(self):
        return f"redis://{self.host}:{self.port}/0"


class FlaskCacheConfig(Config):
    redis: RedisConfig = RedisConfig()
    cash: Cache = Cache()
    cache_config: dict = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": redis.host,
        "CACHE_REDIS_PORT": redis.port,
        "CACHE_REDIS_DB": 0,
        "CACHE_REDIS_URL": redis.url,
    }


class AppConfig(Config):
    secret_key: str
    BASE_DIR: Path = Path()
    template_folder: Path = BASE_DIR / "static/templates/"


class Settings(BaseSettings):

    app: AppConfig = AppConfig()
    flask_cache: FlaskCacheConfig = FlaskCacheConfig()


settings = Settings()
