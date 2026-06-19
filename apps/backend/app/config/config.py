from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
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

    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""

    jwt_secret: str = "change-me-to-a-random-64-char-string"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com"

    nvidia_api_key: str = ""
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"

    linkedin_access_token: str = ""
    linkedin_author_urn: str = ""

    facebook_page_access_token: str = ""
    facebook_page_id: str = ""

    instagram_business_account_id: str = ""

    storage_bucket: str = "campaign-assets"

    comfyui_url: str = "http://localhost:8188"
    comfyui_timeout: int = 600

    allowed_origins: list[str] = ["http://localhost:3000"]

    @property
    def async_database_url(self) -> str:
        if self.database_url.startswith("postgresql+asyncpg://"):
            return self.database_url
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")


settings = Settings()
