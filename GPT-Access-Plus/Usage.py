from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Config import dp, UserState, get_translation, wait
from HelloMessages import menu, profile, payment
import Profile, Payment


@dp.message_handler(state=UserState.usage)
async def usage_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "Usage", "my_profile"):
        await message.answer(wait)
        await UserState.profile.set()
        await profile(chat_id)

    elif message.text == get_translation(language_code, "Usage", "rates"):
        await message.answer(get_translation(language_code, "Usage", "costs"))

    elif message.text == get_translation(language_code, "Usage", "payment"):
        await message.answer(wait)
        await payment(chat_id)

    elif message.text == get_translation(language_code, "Usage", "support"):
        button = InlineKeyboardButton(get_translation(language_code, "Usage", "contact"), url="https://t.me/Alanya2gether")
        kb = InlineKeyboardMarkup().add(button)
        await message.answer(get_translation(language_code, "Usage", "contact_text"), reply_markup= kb)

    elif message.text == get_translation(language_code, "Common", "return_menu"):
        await message.answer(wait)
        await menu(chat_id)
