from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


# https://progressstory.com/tech/configuration-management-python-pydantic/
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "youtube-polling"

    DBUSER: str
    DBPWD: str
    DBHOST: str

    DBPORT: int = 5432
    DBNAME: str = "app_db"

    CONNECTION_STR: str

    # App Config
    POLL_INTERVAL_SECONDS: int = 10
    GOOGLE_DEVELOPER_KEY: str
    YOUTUBE_API_ENDPOINT: str = "https://youtube.googleapis.com/youtube/v3/search"

    # Meta
    DEBUG: bool = False
    LOG_REQUEST_ID: bool = True
    LOG_CORRELATION_ID: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            dotenv_settings,
            file_secret_settings,
            init_settings,
        )


settings = Settings()
