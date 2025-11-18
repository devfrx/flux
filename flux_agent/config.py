"""Configurazione centralizzata."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configurazioni dell'applicazione."""

    #LMStudio
    lmstudio_url: str = "http://127.0.0.1:1234/v1"
    lmstudio_model: str = "google/gemma-3-12b"

    # Database
    database_path: str = "./data/agent.db"

    #logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensititve = False
    )

# Singleton globale
settings = Settings()