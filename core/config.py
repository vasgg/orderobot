import logging

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    ADMIN_ID: int
    CHANNEL_ID: int
    CHANNEL_LINK: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    echo: bool = True

    @property
    def asyncpg_db_url(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()

valid_domains = ['drive.yandex.ru', 'drive.google.com']

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: "
    "%(filename)s: "
    "%(levelname)s: "
    "%(funcName)s(): "
    "%(lineno)d:\t"
    "%(message)s",
)
