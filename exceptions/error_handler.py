import logging
import traceback
from datetime import datetime
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_errors.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def log_error(error: Exception, context: str = "", user_id: int = None):
    """Розширене логування помилок"""
    error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = (
        f"\n{'='*50}\n"
        f"Time: {error_time}\n"
        f"Context: {context}\n"
        f"User ID: {user_id}\n"
        f"Error Type: {type(error).__name__}\n"
        f"Error Message: {str(error)}\n"
        f"Traceback:\n{traceback.format_exc()}\n"
        f"{'='*50}\n"
    )
    logger.error(error_message)


async def safe_edit_message(message: Message, **kwargs):
    """Helper function to safely edit messages with error handling"""
    try:
        await message.edit_text(**kwargs)
    except TelegramBadRequest as e:
        await log_error(
            e,
            f"safe_edit_message - TelegramBadRequest\nMessage ID: {message.message_id}",
            message.chat.id
        )
        if "message is not modified" not in str(e).lower():
            try:
                await message.answer(
                    text=kwargs.get('text', ''),
                    reply_markup=kwargs.get('reply_markup'),
                    parse_mode=kwargs.get('parse_mode')
                )
            except Exception as new_msg_error:
                await log_error(
                    new_msg_error,
                    "safe_edit_message - Failed to send new message",
                    message.chat.id
                )
    except Exception as e:
        await log_error(e, "safe_edit_message - Unexpected error", message.chat.id)