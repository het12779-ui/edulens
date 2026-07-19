"""
Centralized app settings. Loaded once, imported everywhere.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    llm_provider: str = "groq"
    groq_api_key: str = ""
    openai_api_key: str = ""

    whisper_model_size: str = "base"

    supabase_url: str = ""
    supabase_key: str = ""

    upload_dir: str = "./storage/uploads"
    chroma_dir: str = "./storage/chroma"

    env: str = "development"
    frontend_origin: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.chroma_dir, exist_ok=True)
    return settings