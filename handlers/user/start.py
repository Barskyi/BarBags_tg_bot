from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline import main_menu_keyboard
from utils.smt_texts import welcome_text

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    """Обробка команди /start"""
    join_button = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="📢 Приєднатися до каналу",
            url="https://t.me/BarBags_shop"
        )
    ]])

    await message.answer(
        "Вітаємо! Для перегляду нашого каталогу приєднайтесь до каналу:",
        reply_markup=join_button
    )
    await message.answer(
        text=welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )
