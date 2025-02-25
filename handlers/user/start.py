from aiogram import Router, Bot, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters import Command

from config.settings import config, logger
from keyboards.inline import main_menu_keyboard, catalog_keyboard
from utils.commands import set_bot_commands, set_channel_commands
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


@router.message(Command("shares"))
async def menu_command(message: Message):
    """Обробка команди /shares"""
    channel_link = "https://t.me/BarBags_shop/415"

    await message.answer(
        text="<b>Переходьте за посиланням, щоб переглянути наші акції та знижки:</b>\n\n"
             f"<a href='{channel_link}'>🎰 Спеціальні пропозиції</a>",
        parse_mode="HTML",
        disable_web_page_preview=False
    )


@router.message(Command("catalog"))
async def catalog_command(message: Message):
    """Обробка команди /catalog"""
    await message.answer(
        text="Оберіть потрібну категорію:\n👇",
        reply_markup=catalog_keyboard()
    )


@router.message(Command("help"))
async def help_command(message: Message):
    """Обробка команди /help"""
    help_text = """
    🤖 <b>Доступні команди бота:</b>

    /start - Запустити бота
    /menu - Головне меню
    /catalog - Каталог товарів
    /help - Показати цю довідку

    За додатковою допомогою звертайтесь до менеджера @barska_olena
    """
    await message.answer(text=help_text, parse_mode="HTML")


async def pin_webapp_menu():
    """Закріплення повідомлення з веб-додатком у каналі"""
    async with Bot(token=config.BOT_TOKEN) as bot:
        for channel_id in config.CHANNEL_IDS:
            try:
                logger.info(f"Спроба закріплення повідомлення в каналі {channel_id}")
                msg = await bot.send_message(
                    chat_id=channel_id,
                    text=(
                        "<b>🛍 Як оформити замовлення?</b>\n\n"
                        "1️⃣ Оберіть товар у нашому каталозі.\n\n"
                        "2️⃣ Натисніть <a href='https://t.me/barska_olena'>«Написати менеджеру»</a> для консультації.\n\n"
                        "3️⃣ Узгодьте деталі та оплату.\n\n"
                        "4️⃣ Очікуйте швидку доставку! 🚀\n\n"
                        "📢 <b>Корисні посилання:</b>\n\n"
                        "🔹 <a href='https://t.me/barbags_bot'>🏠 Головне меню</a>\n\n"
                        "🔹 <a href='https://t.me/share/url?url=https://t.me/barbags_bot&text=👜 Магазин BarBags: стильні сумки та аксесуари!'>📤 Поділитися</a>\n"
                    ),
                    parse_mode="HTML",
                    reply_markup=types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                types.InlineKeyboardButton(
                                    text="✍️ Написати менеджеру",
                                    url="https://t.me/barska_olena"
                                )
                            ]
                        ]
                    )
                )

                await bot.pin_chat_message(chat_id=channel_id, message_id=msg.message_id)
                logger.info(f"✅ Повідомлення успішно закріплене в каналі {channel_id}")
            except Exception as e:
                logger.error(f"⚠️ Не вдалося закріпити повідомлення в каналі {channel_id}. Помилка: {str(e)}")


async def on_startup():
    """Функція, яка виконується при старті бота"""
    logger.info("📌 Запуск функції закріплення повідомлень...")
    await pin_webapp_menu()

    bot = Bot(token=config.BOT_TOKEN)
    await set_bot_commands(bot)

    for channel_id in config.CHANNEL_IDS:
        await set_channel_commands(bot, channel_id)
    await bot.session.close()
