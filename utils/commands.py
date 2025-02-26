from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from config.settings import logger


async def set_bot_commands(bot: Bot):
    """Встановлення команд для бота"""
    try:
        default_commands = [
            BotCommand(command="start", description="🏠 Запустити бота"),
            BotCommand(command="shares", description="🎰 Акції та знижки"),
            BotCommand(command="catalog", description="🛍 Каталог товарів"),
            BotCommand(command="feedback", description="📣 Наші відгуки"),
            BotCommand(command="help", description="ℹ️ Допомога")
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
            BotCommand(command="catalog", description="🛍 Переглянути каталог"),
            BotCommand(command="manager", description="✍️ Написати менеджеру"),
            BotCommand(command="feedback", description="📣 Наші відгуки")
        ]

        await bot.set_my_commands(
            commands=channel_commands,
            scope=BotCommandScopeChat(chat_id=channel_id)
        )
        logger.info(f"✅ Команди для каналу {channel_id} успішно встановлено")

    except Exception as e:
        logger.error(f"❌ Помилка при встановленні команд для каналу {channel_id}: {e}")
