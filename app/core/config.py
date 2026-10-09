from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Biashara HUB API"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    DATABASE_URL: str = "sqlite:///./biashara_hub.db"
    SECRET_KEY: str = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET_KEY_AT_LEAST_32_BYTES"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    FRONTEND_URL: str = "http://localhost:5173"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,http://127.0.0.1:3000"

    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_CLIENT_SECRET: str = ""
    LINKEDIN_REDIRECT_URI: str = "http://localhost:8000/api/social/linkedin/callback"
    LINKEDIN_SCOPES: str = "openid profile email w_member_social"
    LINKEDIN_API_VERSION: str = "202604"

    META_APP_ID: str = ""
    META_APP_SECRET: str = ""
    META_REDIRECT_URI: str = "http://localhost:8000/api/social/meta/callback"
    META_GRAPH_VERSION: str = "v23.0"
    META_SCOPES: str = "pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish"

    TIKTOK_CLIENT_KEY: str = ""
    TIKTOK_CLIENT_SECRET: str = ""
    TIKTOK_REDIRECT_URI: str = "https://localhost:8000/api/social/tiktok/callback"
    TIKTOK_SCOPES: str = "user.info.basic,video.publish"

    X_CLIENT_ID: str = ""
    X_CLIENT_SECRET: str = ""
    X_REDIRECT_URI: str = "http://localhost:8000/api/social/x/callback"
    X_SCOPES: str = "tweet.read tweet.write users.read offline.access"

    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_BUSINESS_ACCOUNT_ID: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    M_PESA_API_KEY: str = ""
    AIRTEL_MONEY_CLIENT_ID: str = ""
    AIRTEL_MONEY_CLIENT_SECRET: str = ""
    MIXX_CLIENT_ID: str = ""
    HALOPESA_CLIENT_ID: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)

    @property
    def cors_origins(self) -> list[str]:
        return [item.strip() for item in self.CORS_ORIGINS.split(",") if item.strip()]


settings = Settings()
