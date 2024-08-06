from aiogram import executor
from aiogram.types import Message, CallbackQuery
from Webhooks import start_maxpay
from Config import bot, dp, UserState, DB, add_new_user, get_translation, wait
from Keyboards import language_kb
from HelloMessages import menu


@dp.message_handler(commands=['start'], state="*")
async def start(message: Message):
    chat_id = message.chat.id
    await add_new_user(chat_id)
    await UserState.language.set()
    await language_start(chat_id)

import Menu

async def language_start(chat_id):
    await bot.send_message(chat_id, "Choose your language / 选择你的语言 / Выберите язык / Тілді таңдаңыз:", reply_markup=language_kb)

async def language_finish(chat_id, language_code):
    text = get_translation(language_code, "Languages", "language_chosen")
    await bot.send_message(chat_id, text=text)
    await menu(chat_id)


@dp.callback_query_handler(lambda c: 'lang:' in c.data, state=UserState.language)
async def language_chosen(call: CallbackQuery):
    user_id = call.message.chat.id

    await bot.send_message(user_id, wait)

    language_code = call.data.split(":")[1]

    async with DB() as conn:
        await conn.execute('UPDATE user_settings SET language = $1 WHERE user_id = $2', language_code, user_id)

    await language_finish(user_id, language_code)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)