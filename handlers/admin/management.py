from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.connect import async_session
from utils.statistics import StatsManager

router = Router()

ADMIN_IDS = [564324383, 1226589584]  # Замініть на ваш Telegram ID


@router.message(Command("myid"))
async def send_user_id(message: Message):
    await message.answer(f"Ваш Telegram ID: {message.from_user.id}")


@router.message(Command("stats"))
async def show_stats(message: Message):
    """Показує статистику використання бота"""
    if message.from_user.id not in ADMIN_IDS:
        return

    async with async_session() as session:
        stats = StatsManager(session)

        # Отримання загальної статистики
        general_stats = await stats.get_general_stats()
        popular_actions = await stats.get_popular_actions()

        # Форматування повідомлення
        stats_message = (
            "📊 <b>Статистика бота</b>\n\n"
            f"👥 Всього користувачів: {general_stats['total_users']}\n"
            f"📝 Всього дій: {general_stats['total_actions']}\n"
            f"⚡️ Дій за 24 години: {general_stats['actions_24h']}\n\n"
            "🔝 <b>Популярні дії:</b>\n"
        )

        for button_name, count in popular_actions:
            stats_message += f"- {button_name}: {count} разів\n"

        await message.answer(
            stats_message,
            parse_mode="HTML"
        )
