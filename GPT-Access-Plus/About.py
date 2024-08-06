from aiogram.types import Message
from Config import dp, bot, UserState, get_translation, wait
from HelloMessages import menu
import os


@dp.message_handler(state=UserState.about)
async def about_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "About", "about_product"):
        await message.answer(get_translation(language_code, "About", "product"))

    elif message.text == get_translation(language_code, "About", "features"):
        await message.answer(get_translation(language_code, "About", "capabilities"))

    elif message.text == get_translation(language_code, "About", "advantages"):
        await message.answer(get_translation(language_code, "About", "benefits"))

    elif message.text == get_translation(language_code, "About", "fair_game"):
        await message.answer(wait)

        directory_path = f'Documents/{language_code}/'

        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    await bot.send_document(chat_id, file)


    elif message.text == get_translation(language_code, "Common", "return_menu"):
        await message.answer(wait)
        await menu(chat_id)
