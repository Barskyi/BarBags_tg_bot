import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from database.connect import async_session
from database.models import UserAction
from keyboards.inline import main_menu_keyboard, catalog_keyboard, faq_keyboard, wallets_keyboard
from utils.smt_texts import about_text, contact_info, faq_texts
from utils.smt_texts import welcome_text

router = Router()


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
async def handle_catalog_callback(callback: CallbackQuery):
    """Обробка всіх callback кнопок"""
    try:
        async with async_session() as session:
            action = UserAction(
                user_id=callback.from_user.id,
                username=callback.from_user.username,
                action_type="button_click",
                button_name=callback.data,
                message_id=callback.message.message_id
            )
            session.add(action)
            await session.commit()
        if callback.data == "show_catalog":
            await safe_edit_message(
                callback.message,
                text="Оберіть потрібну категорію:\n👇",
                reply_markup=catalog_keyboard()
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
