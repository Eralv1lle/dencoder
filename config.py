from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    database: str
    crypt_key: bytes

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

config = Config() # type: ignore