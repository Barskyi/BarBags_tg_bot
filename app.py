import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config.settings import config
from database.models import init_models
from handlers.admin import management
from handlers.user import start, catalog
from handlers.user.start import on_startup
from middleware.moderator import ModeratorMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    # Створюємо бота за межами try-except
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        logger.info("Ініціалізація бази даних...")
        await init_models()
        logger.info("База даних успішно ініціалізована")

        logger.info("Виконання on_startup функцій...")
        await on_startup()
        logger.info("on_startup функції виконано успішно")

        dp = Dispatcher()

        """Add middleware"""
        dp.message.middleware(ModeratorMiddleware())

        """Router registered"""
        dp.include_router(start.router)
        dp.include_router(catalog.router)
        dp.include_router(management.router)

        logger.info("Бот запущено")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Критична помилка: {e}")
        raise
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
