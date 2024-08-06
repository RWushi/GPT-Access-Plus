from aiogram.types import Message, CallbackQuery
from Config import dp, bot, UserState, get_translation, wait, DB
from ChatDB import get_free_messages
from datetime import datetime, timezone
from HelloMessages import usage
from Keyboards import language_kb


@dp.message_handler(state=UserState.profile)
async def profile_handler(message: Message):
    language_code = message.conf.get('language_code')
    user_id = message.from_user.id

    if message.text == get_translation(language_code, "Profile", "trial_requests"):
        free_messages_left = await get_free_messages(user_id)
        await message.answer(f"{get_translation(language_code, 'Profile', 'remaining')} {free_messages_left}")

    elif message.text == get_translation(language_code, "Profile", "my_subscription"):
        async with DB() as conn:
            subscription_end_date = await conn.fetchval("SELECT subscription_end_date FROM user_subscriptions WHERE user_id = $1", user_id)

        if subscription_end_date is None:
            await message.answer(get_translation(language_code, "Profile", "no_active_subscription"))
        elif subscription_end_date < datetime.now(timezone.utc):
            formatted_date = subscription_end_date.strftime('%Y-%m-%d %H:%M:%S UTC')
            await message.answer(f"{get_translation(language_code, 'Profile', 'subscription_expired')}\n{formatted_date}")
        else:
            formatted_date = subscription_end_date.strftime('%Y-%m-%d %H:%M:%S UTC')
            await message.answer(get_translation(language_code, "Profile", "you_have_subscription"))
            await message.answer(f"{get_translation(language_code, 'Profile', 'subscription_end')}\n{formatted_date}\n{get_translation(language_code, 'Profile', 'real_end')}")

    elif message.text == get_translation(language_code, "Profile", "my_id"):
        await message.answer(f"{get_translation(language_code, 'Profile', 'your_id')} {user_id}\n{get_translation(language_code, 'Profile', 'id_info')}")

    elif message.text == get_translation(language_code, "Profile", "change_language"):
        await message.answer(get_translation(language_code, "Profile", "choose_language"), reply_markup=language_kb)

    elif message.text == get_translation(language_code, "Common", "return_back"):
        await message.answer(wait)
        await usage(message.chat.id)


@dp.callback_query_handler(lambda c: 'lang:' in c.data, state=UserState.profile)
async def language_chosen(call: CallbackQuery):
    user_id = call.message.chat.id

    await bot.send_message(user_id, wait)

    language_code = call.data.split(":")[1]

    async with DB() as conn:
        await conn.execute('UPDATE user_settings SET language = $1 WHERE user_id = $2', language_code, user_id)

    await bot.send_message(user_id, get_translation(language_code, "Profile", "language_changed"))