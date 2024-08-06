from aiogram.types import Message
from Config import dp, UserState, get_translation, wait, DB
from HelloMessages import customization


@dp.message_handler(state=UserState.style)
async def style_handler(message: Message):
    language_code = message.conf.get('language_code')
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "SubCommon", "view_example"):
        await message.answer(get_translation(language_code, "Style", "example"))

    elif message.text == get_translation(language_code, "Style", "current_style"):
        async with DB() as conn:
            style = await conn.fetchval('SELECT style FROM user_settings WHERE user_id = $1', user_id)
        if style:
            await message.answer(f"{get_translation(language_code, 'Style', 'current')} {style}")
        else:
            await message.answer(get_translation(language_code, "Style", "not_set"))

    elif message.text == get_translation(language_code, "Style", "reset_style"):
        async with DB() as conn:
            await conn.execute("UPDATE user_settings SET style = NULL WHERE user_id = $1", user_id)
        await message.answer(get_translation(language_code, "Style", "reset"))

    elif message.text == get_translation(language_code, "Common", "return_back"):
        await message.answer(wait)
        await customization(chat_id)

    else:
        style = message.text
        async with DB() as conn:
            await conn.execute('''
                INSERT INTO user_settings (user_id, style) 
                VALUES ($1, $2) 
                ON CONFLICT (user_id) DO UPDATE SET style = $2
            ''', user_id, style)
        await message.answer(get_translation(language_code, "Style", "applied"))

