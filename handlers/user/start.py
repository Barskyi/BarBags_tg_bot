from aiogram import Router, Bot, types
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.settings import config, logger
from keyboards.inline import main_menu_keyboard
from utils.smt_texts import welcome_text

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    """Обробка команди /start"""
    await message.answer(
        text=welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )


async def pin_webapp_menu():
    """Закріплення повідомлення з веб-додатком у каналі"""
    async with Bot(token=config.BOT_TOKEN) as bot:
        for channel_id in config.CHANNEL_IDS:
            try:
                logger.info(f"Спроба закріплення повідомлення в каналі {channel_id}")
                msg = await bot.send_message(
                    chat_id=channel_id,
                    text="🛒 Для замовлення: ",
                    reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                        [types.InlineKeyboardButton(
                            text=" ✍️ Написати менеджеру",
                            url="https://t.me/barska_olenka"
                        )]
                    ])
                )
                await bot.pin_chat_message(chat_id=channel_id, message_id=msg.message_id)
                logger.info(f"✅ Повідомлення успішно закріплене в каналі {channel_id}")
            except Exception as e:
                logger.error(f"⚠️ Не вдалося закріпити повідомлення в каналі {channel_id}. Помилка: {str(e)}")


async def on_startup():
    """Функція, яка виконується при старті бота"""
    logger.info("📌 Запуск функції закріплення повідомлень...")
    await pin_webapp_menu()
