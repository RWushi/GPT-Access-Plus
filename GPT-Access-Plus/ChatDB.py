from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from datetime import datetime, timezone
import json
from Config import dp, bot, DB, UserState, get_language, get_translation
from Keyboards import prechat_kb


async def save_history(user_id, history):
    history_str = json.dumps(history)

    async with DB() as conn:
        await conn.execute('''
            INSERT INTO user_settings (user_id, chat_history) 
            VALUES ($1, $2) 
            ON CONFLICT (user_id) DO UPDATE SET chat_history = $2
        ''', user_id, history_str)


async def reset_history(user_id):
    empty_history = json.dumps([])

    async with DB() as conn:
        await conn.execute('''
            UPDATE user_settings SET chat_history = $1 WHERE user_id = $2
        ''', empty_history, user_id)


async def get_user_data(user_id):
    async with DB() as conn:
        row = await conn.fetchrow('SELECT chat_history, style, information FROM user_settings WHERE user_id = $1', user_id)

    if row is None:
        return None, None, None

    history = json.loads(row['chat_history']) if row['chat_history'] else []

    return history, row['style'], row['information']

async def get_free_messages(user_id):
    async with DB() as conn:
        free_messages_left = await conn.fetchval('SELECT free_messages_left FROM user_subscriptions WHERE user_id = $1', user_id)
    return free_messages_left

async def decrement_free_messages(user_id):
    async with DB() as conn:
        await conn.execute('UPDATE user_subscriptions SET free_messages_left = free_messages_left - 1 WHERE user_id = $1', user_id)

async def has_free_messages(user_id):
    language_code = await get_language(user_id)
    free_messages_left = await get_free_messages(user_id)
    if free_messages_left > 0:
        return True
    else:
        await bot.send_message(user_id, get_translation(language_code, "ChatDB", "no_free_queries"))
        return False

async def pre_check_vip(user_id):
    language_code = await get_language(user_id)
    async with DB() as conn:
        end_date = await conn.fetchval('SELECT subscription_end_date FROM user_subscriptions WHERE user_id = $1', user_id)

    if end_date is None:
        await bot.send_message(user_id, get_translation(language_code, "ChatDB", "need_subscription_for_vip"))
        return False

    elif datetime.now(timezone.utc) > end_date:
        await bot.send_message(user_id, get_translation(language_code, "ChatDB", "subscription_expired"))
        return False

    else:
        await bot.send_message(user_id, get_translation(language_code, "ChatDB", "verification_successful"))
        await bot.send_sticker(user_id, "CAACAgIAAxkBAAIQAWUlEp7AtYdnYjZD5V5FtrfMb7mZAAI_EQACQQipSKePgWazX2l2MAQ")
        return True


async def pre_check_free(user_id):
    language_code = await get_language(user_id)
    async with DB() as conn:
        end_date = await conn.fetchval('SELECT subscription_end_date FROM user_subscriptions WHERE user_id = $1', user_id)

    if end_date is not None and datetime.now(timezone.utc) <= end_date:
        await bot.send_message(user_id, get_translation(language_code, "ChatDB", "active_subscription"))
        return False
    return True


async def expired(user_id):
    language_code = await get_language(user_id)
    async with DB() as conn:
        current_state = await conn.fetchval('SELECT user_state FROM user_settings WHERE user_id = $1', user_id)

    if current_state == 'UserState:chatvip':
        await dp.current_state(chat=user_id).set_state(UserState.prechat.state)

        await bot.send_message(user_id, get_translation(language_code, "ChatDB", "renew_for_vip"), reply_markup=prechat_kb(language_code))
    else:
        await bot.send_message(user_id, get_translation(language_code, "ChatDB", "renew_for_vip"))

async def check_subscription_daily():
    async with DB() as conn:
        user_list = await conn.fetch('SELECT user_id FROM user_subscriptions WHERE subscription_end_date < $1', datetime.now(timezone.utc))

    for record in user_list:
        user_id = record['user_id']
        await expired(user_id)


scheduler = AsyncIOScheduler()
scheduler.add_job(check_subscription_daily, 'cron', hour=0, minute=0, timezone=utc)
scheduler.start()