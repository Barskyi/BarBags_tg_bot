from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    DATABASE_URL: str = os.getenv('DATABASE_URL', '')

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            if self.DATABASE_URL.startswith("postgres://"):
                return self.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Fallback для локальної розробки
        db_user = os.getenv('DB_USER', 'postgres')
        db_pass = os.getenv('DB_PASS', '')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'barbags_bot')
        return f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


config = Config()

if not config.BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено! Переконайтесь, що .env файл містить BOT_TOKEN")