from dataclasses import dataclass
from typing import List, Optional
from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


@dataclass
class MenuItem:
    text: str
    callback_data: Optional[str] = None
    url: Optional[str] = None
    web_app_url: Optional[str] = None
    switch_inline_query: Optional[str] = None


class MenuBuilder:
    def __init__(self, items: List[MenuItem]):
        self.items = items

    def build(self) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()

        for item in self.items:
            button_params = {"text": item.text}

            if item.callback_data:
                button_params["callback_data"] = item.callback_data
            elif item.url:
                button_params["url"] = item.url
            elif item.web_app_url:
                button_params["web_app"] = WebAppInfo(url=item.web_app_url)
            elif item.switch_inline_query:
                button_params["switch_inline_query"] = item.switch_inline_query

            builder.add(InlineKeyboardButton(**button_params))

        builder.adjust(1)
        return builder.as_markup()  # type: ignore
