from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Marketing OS"
    app_version: str = "0.1.0"
    app_env: str = "development"
    app_debug: bool = True
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://localhost:5432/ai_marketing_os"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "change-me-to-a-random-64-char-string"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    nvidia_api_key: str = ""
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"

    sc_api_key: str = ""

    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_name: str = "ai-marketing-assets"
    r2_public_url: str = ""

    comfyui_url: str = "http://localhost:8188"
    comfyui_timeout: int = 600

    allowed_origins: list[str] = ["http://localhost:3000"]

    @property
    def async_database_url(self) -> str:
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")


settings = Settings()
