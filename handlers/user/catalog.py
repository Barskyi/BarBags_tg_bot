import logging
import traceback

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.connect import async_session
from database.models import UserAction
from keyboards.inline import main_menu_keyboard, catalog_keyboard, faq_keyboard, wallets_keyboard
from utils.smt_texts import about_text, faq_texts
from utils.smt_texts import welcome_text

router = Router()

CHANNEL_USERNAME = "@BarBags_shop"


async def check_subscription(bot, user_id: int) -> bool:
    """Перевіряє, чи користувач підписаний на канал."""
    try:
        chat_member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ("member", "administrator", "creator")
    except Exception as e:
        logging.error(f"Помилка при перевірці підписки: {e}")
        return False


async def safe_edit_message(message, **kwargs):
    """Helper function to safely edit messages with error handling"""
    try:
        await message.edit_text(**kwargs)
    except TelegramBadRequest as e:
        logging.error(f"Failed to edit message: {e}")
        if "message is not modified" not in str(e).lower():
            try:
                await message.answer(
                    text=kwargs.get('text', ''),
                    reply_markup=kwargs.get('reply_markup'),
                    parse_mode=kwargs.get('parse_mode')
                )
            except Exception as new_msg_error:
                logging.error(f"Failed to send new message: {new_msg_error}")
    except Exception as e:
        logging.error(f"Unexpected error while editing message: {e}")


@router.callback_query(F.data)
async def handle_catalog_callback(callback: CallbackQuery, bot):
    """Обробка всіх callback кнопок"""
    try:
        async with async_session() as session:
            user = callback.from_user
            user_identifier = user.username or f"{user.first_name} {user.last_name or ''}".strip() or f"user_{user.id}"

            action = UserAction(
                user_id=callback.from_user.id,
                username=user_identifier,
                action_type="button_click",
                button_name=callback.data,
                message_id=callback.message.message_id
            )
            session.add(action)
            await session.commit()

        if callback.data == "show_catalog":
            is_subscribed = await check_subscription(bot, callback.from_user.id)

            if is_subscribed:
                try:
                    await safe_edit_message(
                        callback.message,
                        text="Оберіть потрібну категорію:\n👇",
                        reply_markup=catalog_keyboard()
                    )
                except Exception as e:
                    logging.error(f"Error in handle_catalog_callback: {e}\n{traceback.format_exc()}")
                    await callback.message.answer(
                        text="Оберіть потрібну категорію:\n👇",
                        reply_markup=catalog_keyboard()
                    )
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔔 Підписатися", url=f"https://t.me/{CHANNEL_USERNAME}")],
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
                    await callback.message.answer(
                        text="Щоб переглянути каталог, необхідно підписатися на наш канал!",
                        reply_markup=keyboard
                    )

        elif callback.data == "check_subscription":
            if await check_subscription(bot, callback.from_user.id):
                try:
                    await safe_edit_message(
                        callback.message,
                        text="✅ Ви підписані! Ось каталог:",
                        reply_markup=catalog_keyboard()
                    )
                except Exception as e:
                    await callback.message.answer(
                        text="✅ Ви підписані! Ось каталог:",
                        reply_markup=catalog_keyboard()
                    )
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔔 Підписатися", url=f"https://t.me/{CHANNEL_USERNAME}")],
                    [InlineKeyboardButton(text="✅ Перевірити", callback_data="check_subscription")],
                    [InlineKeyboardButton(text="↩️ Головне меню", callback_data="main_menu")]
                ])
                try:
                    await safe_edit_message(
                        callback.message,
                        text="❌ Ви ще не підписані. Будь ласка, підпишіться та спробуйте знову.",
                        reply_markup=keyboard
                    )
                except Exception as e:
                    await callback.message.answer(
                        text="❌ Ви ще не підписані. Будь ласка, підпишіться та спробуйте знову.",
                        reply_markup=keyboard
                    )
        elif callback.data == "main_menu":
            await safe_edit_message(
                callback.message,
                text=welcome_text,
                reply_markup=main_menu_keyboard()
            )

        elif callback.data == "about_us":
            await safe_edit_message(
                callback.message,
                text=about_text,
                reply_markup=main_menu_keyboard(),
                parse_mode="HTML"
            )

        elif callback.data == "faq":
            await safe_edit_message(
                callback.message,
                text="Оберіть розділ, який вас цікавить:",
                reply_markup=faq_keyboard()
            )

        elif callback.data in {"delivery_info", "payment_info", "return_info", "warranty_info"}:
            await safe_edit_message(
                callback.message,
                text=faq_texts[callback.data],
                reply_markup=faq_keyboard(),
                parse_mode="HTML"
            )
        elif callback.data == "show_wallets":
            await safe_edit_message(
                callback.message,
                text="Оберіть категорію гаманців:\n👇",
                reply_markup=wallets_keyboard()
            )

        try:
            await callback.answer()
        except Exception as e:
            logging.error(f"Failed to answer callback: {e}")

    except Exception as e:
        logging.error(f"Error in handle_catalog_callback: {e}")
        try:
            await callback.message.answer("Вибачте, сталася помилка. Спробуйте ще раз.")
        except:
            pass
