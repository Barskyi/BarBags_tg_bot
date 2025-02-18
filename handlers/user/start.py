from aiogram import Router, Bot, types
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.settings import config, logger
from keyboards.inline import main_menu_keyboard
from utils.smt_texts import welcome_text

router = Router()

# BOT_TOKEN = os.getenv("BOT_TOKEN", "")
# CHANNEL_IDS = [int(ch_id) for ch_id in os.getenv("CHANNEL_IDS", "").split(",") if ch_id.strip().isdigit()]

# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN не знайдено! Переконайтесь, що .env файл містить BOT_TOKEN")


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
    bot = Bot(token=config.BOT_TOKEN)
    channel_ids = config.CHANNEL_IDS

    for channel_id in channel_ids:
        try:
            msg = await bot.send_message(
                chat_id=channel_id,
                text="🛒 Для замовлення натисніть кнопку нижче 👇",
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(
                        text="🛍 Відкрити каталог",
                        web_app=types.WebAppInfo(url="https://barskyi.github.io/for_order.html")
                    )]
                ])
            )
            await bot.pin_chat_message(chat_id=channel_id, message_id=msg.message_id)
            logger.info(f"✅ Повідомлення закріплене в каналі {channel_id}")
        except Exception as e:
            logger.error(f"⚠️ Не вдалося закріпити повідомлення в {channel_id}: {e}")

    await bot.session.close()


async def on_startup():
    """Функція, яка виконується при старті бота"""
    await pin_webapp_menu()
