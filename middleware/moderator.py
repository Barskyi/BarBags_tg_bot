from string import punctuation
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from utils.smt_texts import restricted_words


def clean_text(text: str) -> str:
    return text.translate(str.maketrans("", "", punctuation))


class ModeratorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not event.text:
            return await handler(event, data)

        clean_message = clean_text(event.text.lower())
        if restricted_words.intersection(clean_message.split()):
            await event.delete()
            return

        return await handler(event, data)
