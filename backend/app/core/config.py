from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Job Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = ""

    GEMINI_API_KEY: str = "AIzaSyCBAfYQpAwuaZedbdP56mXcFjvuk2TaGes"
    JSEARCH_API_KEY: str = "506c3916c4mshc9c46a496e77e75p12b1f7jsn56d6919bebcd"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()