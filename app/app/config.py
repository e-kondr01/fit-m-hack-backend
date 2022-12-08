from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn, validator

load_dotenv()

ROOT_DIR = Path(__file__).resolve(strict=True).parent


class Settings(BaseSettings):

    SECRET_KEY = "ASDV5w41r64564b1u65416s5e4rt1bASDFVad4fq5"

    # PostgreSQL Database Connection
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URL: PostgresDsn | None

    @validator("SQLALCHEMY_DATABASE_URL", pre=True)
    def assemble_db_connection_string(
        cls, value: PostgresDsn | None, values: dict[str, Any]
    ) -> Any:
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            host=values["POSTGRES_HOST"],
            port=values["POSTGRES_PORT"],
            path=f"/{values['POSTGRES_DB']}",
        )

    class Config:
        case_sensitive = True


settings = Settings()
