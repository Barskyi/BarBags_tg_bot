from dataclasses import dataclass
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    DATABASE_URL: str = os.getenv('DATABASE_URL', '')
    CHANNEL_IDS: list[str] = None

    def __post_init__(self):
        """Перетворюємо CHANNEL_IDS у список чисел"""
        channel_ids_str = os.getenv("CHANNEL_IDS", "")
        logger.info(f"📌 Отримано CHANNEL_IDS зі змінних оточення: '{channel_ids_str}'")

        if channel_ids_str:
            try:
                self.CHANNEL_IDS = [ch_id.strip() for ch_id in channel_ids_str.split(",") if ch_id.strip()]
                logger.info(f"📌 Завантажено ID каналів: {self.CHANNEL_IDS}")
            except Exception as e:
                logger.error(f"❌ Помилка при обробці CHANNEL_IDS: {e}")
                self.CHANNEL_IDS = []
        else:
            self.CHANNEL_IDS = []
            logger.warning("⚠️ CHANNEL_IDS не знайдено або порожній!")

        logger.info(f"📌 Фінальне значення CHANNEL_IDS: {self.CHANNEL_IDS}")

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            logger.info(
                f"Using DATABASE_URL from environment: {self.DATABASE_URL[:15]}...")
            if self.DATABASE_URL.startswith("postgres://"):
                return self.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

        logger.warning("DATABASE_URL not found, using fallback configuration")
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
