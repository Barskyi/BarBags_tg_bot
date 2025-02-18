from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.connect import async_session
from database.models import UserAction
from keyboards.inline import main_menu_keyboard, catalog_keyboard, faq_keyboard, wallets_keyboard
from utils.smt_texts import about_text, faq_texts, welcome_text
from exceptions.error_handler import log_error, safe_edit_message

router = Router()

CHANNEL_USERNAME = "@BarBags_shop"


async def check_subscription(bot, user_id: int) -> bool:
    """Перевіряє, чи користувач підписаний на канал."""
    try:
        chat_member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ("member", "administrator", "creator")
    except Exception as e:
        await log_error(e, "check_subscription", user_id)
        return False


@router.callback_query(F.data)
async def handle_catalog_callback(callback: CallbackQuery, bot):
    """Обробка всіх callback кнопок"""
    user_id = callback.from_user.id

    try:
        # Logging user action
        async with async_session() as session:
            try:
                user = callback.from_user
                user_identifier = user.username or f"{user.first_name} {user.last_name or ''}".strip() or f"user_{user.id}"

                action = UserAction(
                    user_id=user_id,
                    username=user_identifier,
                    action_type="button_click",
                    button_name=callback.data,
                    message_id=callback.message.message_id
                )
                session.add(action)
                await session.commit()
            except Exception as db_error:
                await log_error(db_error, "Database operation failed", user_id)

        # Handle different callback types
        if callback.data == "show_catalog":
            is_subscribed = await check_subscription(bot, user_id)

            if is_subscribed:
                try:
                    await safe_edit_message(
                        callback.message,
                        text="Оберіть потрібну категорію:\n👇",
                        reply_markup=catalog_keyboard()
                    )
                except Exception as e:
                    await log_error(e, "show_catalog - subscribed user", user_id)
                    await callback.message.answer(
                        text="Оберіть потрібну категорію:\n👇",
                        reply_markup=catalog_keyboard()
                    )
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔔 Підписатися", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                    [InlineKeyboardButton(text="✅ Перевірити", callback_data="check_subscription")],
                    [InlineKeyboardButton(text="↩️ Головне меню", callback_data="main_menu")]
                ])
                try:
                    await safe_edit_message(
                        callback.message,
                        text="Щоб переглянути каталог, необхідно підписатися на наш канал!",
                        reply_markup=keyboard
                    )
                except Exception as e:
                    await log_error(e, "show_catalog - unsubscribed user", user_id)
                    await callback.message.answer(
                        text="Щоб переглянути каталог, необхідно підписатися на наш канал!",
                        reply_markup=keyboard
                    )

        elif callback.data == "check_subscription":
            try:
                is_subscribed = await check_subscription(bot, user_id)
                if is_subscribed:
                    await safe_edit_message(
                        callback.message,
                        text="✅ Ви підписані! Ось каталог:",
                        reply_markup=catalog_keyboard()
                    )
                else:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="🔔 Підписатися", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
                        [InlineKeyboardButton(text="✅ Перевірити", callback_data="check_subscription")],
                        [InlineKeyboardButton(text="↩️ Головне меню", callback_data="main_menu")]
                    ])
                    await safe_edit_message(
                        callback.message,
                        text="❌ Ви ще не підписані. Будь ласка, підпишіться та спробуйте знову.",
                        reply_markup=keyboard
                    )
            except Exception as e:
                await log_error(e, "check_subscription callback", user_id)
                await callback.message.answer(
                    text="Виникла помилка при перевірці підписки. Спробуйте ще раз.",
                    reply_markup=main_menu_keyboard()
                )

        elif callback.data == "main_menu":
            try:
                await safe_edit_message(
                    callback.message,
                    text=welcome_text,
                    reply_markup=main_menu_keyboard()
                )
            except Exception as e:
                await log_error(e, "main_menu", user_id)

        elif callback.data == "about_us":
            try:
                await safe_edit_message(
                    callback.message,
                    text=about_text,
                    reply_markup=main_menu_keyboard(),
                    parse_mode="HTML"
                )
            except Exception as e:
                await log_error(e, "about_us", user_id)

        elif callback.data == "faq":
            try:
                await safe_edit_message(
                    callback.message,
                    text="Оберіть розділ, який вас цікавить:",
                    reply_markup=faq_keyboard()
                )
            except Exception as e:
                await log_error(e, "faq", user_id)

        elif callback.data in {"delivery_info", "payment_info", "return_info", "warranty_info"}:
            try:
                await safe_edit_message(
                    callback.message,
                    text=faq_texts[callback.data],
                    reply_markup=faq_keyboard(),
                    parse_mode="HTML"
                )
            except Exception as e:
                await log_error(e, f"faq_section: {callback.data}", user_id)

        elif callback.data == "show_wallets":
            try:
                await safe_edit_message(
                    callback.message,
                    text="Оберіть категорію гаманців:\n👇",
                    reply_markup=wallets_keyboard()
                )
            except Exception as e:
                await log_error(e, "show_wallets", user_id)

        try:
            await callback.answer()
        except Exception as e:
            await log_error(e, "callback answer", user_id)

    except Exception as e:
        await log_error(e, "handle_catalog_callback - main handler", user_id)
        try:
            await callback.message.answer(
                text="Вибачте, сталася помилка. Спробуйте ще раз.",
                reply_markup=main_menu_keyboard()
            )
        except Exception as answer_error:
            await log_error(answer_error, "Failed to send error message", user_id)
