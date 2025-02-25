from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from config.settings import logger


async def set_bot_commands(bot: Bot):
    """Встановлення команд для бота"""
    try:
        # Створюємо лише одну команду для акцій
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


async def set_channel_commands(bot: Bot, channel_id: str):
    """Встановлення команд для конкретного каналу"""
    try:
        channel_commands = [
            BotCommand(command="menu", description="🔥 Акції")
        ]

        await bot.set_my_commands(
            commands=channel_commands,
            scope=BotCommandScopeChat(chat_id=channel_id)
        )
        logger.info(f"✅ Команди для каналу {channel_id} успішно встановлено")

    except Exception as e:
        logger.error(f"❌ Помилка при встановленні команд для каналу {channel_id}: {e}")


async def delete_all_commands(bot: Bot):
    """Видалення всіх команд бота"""
    try:
        await bot.delete_my_commands(scope=BotCommandScopeDefault())
        logger.info("✅ Всі команди бота успішно видалено")
    except Exception as e:
        logger.error(f"❌ Помилка при видаленні команд бота: {e}")
