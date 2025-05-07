import os

from dotenv import load_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.getcwd(), "../", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    POSTGRES_HOST: str = Field(...)
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: SecretStr = Field(...)
    POSTGRES_PORT: str = Field(...)
    POSTGRES_DB: str = Field(...)
    JWT_SECRET: str = Field(...)
    JWT_ALGORITHM: str = Field(...)

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        password = self.POSTGRES_PASSWORD.get_secret_value()
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{password}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
