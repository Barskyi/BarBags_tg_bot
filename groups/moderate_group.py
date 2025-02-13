from string import punctuation

from aiogram import Router, types

from utils.smt_texts import restricted_words

user_group_router = Router()


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.message()
async def cleaner(message: types.Message):
    if not message.text:
        return

    clean_message = clean_text(message.text.lower())
    if restricted_words.intersection(clean_message.split()):
        await message.delete()

