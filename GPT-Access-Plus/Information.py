from aiogram.types import Message
from Config import dp, UserState, get_translation, wait, DB
from HelloMessages import customization


@dp.message_handler(state=UserState.information)
async def information_handler(message: Message):
    language_code = message.conf.get('language_code')
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "SubCommon", "view_example"):
        await message.answer(get_translation(language_code, "Information", "example"))

    elif message.text == get_translation(language_code, "Information", "current_info"):
        async with DB() as conn:
            information = await conn.fetchval('SELECT information FROM user_settings WHERE user_id = $1', user_id)
        if information:
            await message.answer(f"{get_translation(language_code, 'Information', 'current')} {information}")
        else:
            await message.answer(get_translation(language_code, "Information", "not_set"))

    elif message.text == get_translation(language_code, "Information", "reset_info"):
        async with DB() as conn:
            await conn.execute("UPDATE user_settings SET information = NULL WHERE user_id = $1", user_id)
        await message.answer(get_translation(language_code, "Information", "reset"))

    elif message.text == get_translation(language_code, "Common", "return_back"):
        await message.answer(wait)
        await customization(chat_id)

    else:
        information = message.text
        async with DB() as conn:
            await conn.execute('''
                INSERT INTO user_settings (user_id, information) 
                VALUES ($1, $2) 
                ON CONFLICT (user_id) DO UPDATE SET information = $2
            ''', user_id, information)
        await message.answer(get_translation(language_code, "Information", "applied"))