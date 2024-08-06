from aiogram.types import Message
from Config import dp, UserState, get_translation, wait
from HelloMessages import menu, style, information
import Style, Information


@dp.message_handler(state=UserState.customization)
async def customization_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "Customization", "set_style"):
        await message.answer(wait)
        await style(chat_id)

    elif message.text == get_translation(language_code, "Customization", "set_info"):
        await message.answer(wait)
        await information(chat_id)

    elif message.text == get_translation(language_code, "Subcommon", "what_is_this"):
        await message.answer(get_translation(language_code, "Customization", "description"))

    elif message.text == get_translation(language_code, "Common", "return_menu"):
        await message.answer(wait)
        await menu(chat_id)