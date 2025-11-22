from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Customer Support Agent"
    API_V1_PREFIX: str = "/api"
    ENV: str = "development"

    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "supportdb"
    POSTGRES_USER: str = "supportuser"
    POSTGRES_PASSWORD: str = "supportpassword"

    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_SUPER_SECRET"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    HF_API_TOKEN: str = ""
    HF_TEXTGEN_MODEL_ID: str = "google/gemma-2-2b-it"
    HF_CLASSIFIER_MODEL_ID: str = "facebook/bart-large-mnli"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        if isinstance(v, list):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
