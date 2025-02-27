from aiogram import Bot, types

from config.settings import config, logger


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
