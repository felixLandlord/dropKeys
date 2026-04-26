from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    database_url: str
    google_redirect_uri: str
    upstash_redis_rest_url: str
    upstash_redis_rest_token: str


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()

os.environ["GOOGLE_CLIENT_ID"] = settings.google_client_id
os.environ["GOOGLE_CLIENT_SECRET"] = settings.google_client_secret
os.environ.setdefault("GOOGLE_REDIRECT_URI", settings.google_redirect_uri)