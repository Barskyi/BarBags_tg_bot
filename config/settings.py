from dataclasses import dataclass

from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PASS: str = os.getenv('DB_PASS', '')
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: str = os.getenv('DB_PORT', '5432')
    DB_NAME: str = os.getenv('DB_NAME', 'barbags_bot')

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


config = Config()


if not config.BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено! Переконайтесь, що .env файл містить BOT_TOKEN")