from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, ReplyKeyboardMarkup, KeyboardButton
from config.settings import logger


async def set_bot_commands(bot: Bot):
    """Встановлення команд для бота"""
    try:
        default_commands = [
            BotCommand(command="menu", description="🔥 Акції")
        ]

        await bot.set_my_commands(
            commands=default_commands,
            scope=BotCommandScopeDefault()
        )
        logger.info("✅ Команди бота успішно встановлено")

    except Exception as e:
        logger.error(f"❌ Помилка при встановленні команд бота: {e}")


async def delete_all_commands(bot: Bot):
    """Видалення всіх команд бота"""
    try:
        await bot.delete_my_commands(scope=BotCommandScopeDefault())
        logger.info("✅ Всі команди бота успішно видалено")
    except Exception as e:
        logger.error(f"❌ Помилка при видаленні команд бота: {e}")


def get_main_keyboard():
    """Головна клавіатура"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔥 Акції")],
        ],
        resize_keyboard=True
    )
