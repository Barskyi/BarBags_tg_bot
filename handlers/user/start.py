import os

from aiogram import Router, Bot, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.inline import main_menu_keyboard
from utils.smt_texts import welcome_text

router = Router()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено! Переконайтесь, що .env файл містить BOT_TOKEN")


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
    bot = Bot(token=BOT_TOKEN)
    msg = await bot.send_message(
        chat_id=CHANNEL_ID,
        text="🛒 Для замовлення натисніть кнопку нижче 👇",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text="🛍 Відкрити каталог",
                web_app=types.WebAppInfo(url="https://barskyi.github.io/for_order.html")
            )]
        ])
    )
    await bot.pin_chat_message(chat_id=CHANNEL_ID, message_id=msg.message_id)
