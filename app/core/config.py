from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized production-ready application configuration.
    """

    APP_NAME: str = "AI Data Pipeline"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "phi"

    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""
    EMAIL_TO: str = ""

    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    DASHBOARD_HOST: str = "127.0.0.1"
    DASHBOARD_PORT: int = 8050

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()