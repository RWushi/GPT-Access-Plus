from aiogram.types import Message
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from Config import bot, dp, UserState, get_translation, wait, DB, create_connection
from HelloMessages import usage
import aiohttp, bcrypt


@dp.message_handler(state=UserState.payment)
async def payment_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "Payment", "1_month"):
        await message.answer(wait)
        await request_invoice(chat_id, get_translation(language_code, "Payment", "description_1_month"), 7080, 1)

    elif message.text == get_translation(language_code, "Payment", "3_months"):
        await message.answer(wait)
        await request_invoice(chat_id, get_translation(language_code, "Payment", "description_3_months"), 18880, 3)

    elif message.text == get_translation(language_code, "Payment", "6_months"):
        await message.answer(wait)
        await request_invoice(chat_id, get_translation(language_code, "Payment", "description_6_months"), 33040, 6)

    elif message.text == get_translation(language_code, "Payment", "12_months"):
        await message.answer(wait)
        await request_invoice(chat_id, get_translation(language_code, "Payment", "description_12_months"), 56640, 12)

    elif message.text == get_translation(language_code, "Common", "return_back"):
        await message.answer(wait)
        await usage(message.chat.id)


async def get_order_number(user_id):
    async with DB() as conn:
        order_number = await conn.fetchval("""
            INSERT INTO user_subscriptions (user_id, order_number)
            VALUES ($1, 1)
            ON CONFLICT (user_id)
            DO UPDATE SET order_number = user_subscriptions.order_number + 1
            RETURNING order_number
        """, user_id)

    return order_number


def generate_signature(reference_id, secret_key):
    combined_string = f"{reference_id}{secret_key}".encode()
    hashed = bcrypt.hashpw(combined_string, bcrypt.gensalt())
    return hashed


async def request_invoice(chat_id, description, amount, period):
    order_number = await get_order_number(chat_id)
    reference_id = f"{chat_id}_{order_number}"
    signature = generate_signature(reference_id, '341728').decode('utf-8')

    url = "https://api.maxpay.kz/test/invoices/payin"
    data = {
        "merchant_id": "5",
        "secret_key": signature,
        "is_test": "1",
        "reference_id": reference_id,
        "user_id": "58932",
        "amount": amount,
        "period": period,
        "currency": "KZT",
        "description": description,
        "request_url": "https://t.me/ChatGPT4AccessPlus_bot",
        "failure_url": "https://t.me/ChatGPT4AccessPlus_bot",
        "back_url": "https://bc76-185-117-121-93.ngrok.io/webhooks/maxpay"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            response_data = await response.json()
            if response_data.get("success"):
                payment_url = response_data["data"]["redirect_url"]
                await bot.send_message(chat_id, payment_url)
            else:
                error_message = response_data.get("message", "Ошибка при создании ссылки на оплату, выберите другую платежную систему или обратитесь в поддержку")
                await bot.send_message(chat_id, error_message)


async def month_declination(period):
    if period == '1':
        months_word = "месяц"
    elif period == '3':
        months_word = "месяца"
    elif period == '6' or period == '12':
        months_word = "месяцев"
    return months_word


async def subscription_status(user_id, period, conn):
    current_end_date = await conn.fetchval('SELECT subscription_end_date FROM user_subscriptions WHERE user_id = $1', user_id)
    await conn.close()
    now_utc = datetime.now(timezone.utc)

    if current_end_date is None:
        new_end_date = now_utc + relativedelta(months=period)
        msg = "Поздравляем! Теперь Вы являетесь подписчиком GPT-4 Access Plus"
    elif current_end_date < now_utc:
        new_end_date = now_utc + relativedelta(months=period)
        msg = "Поздравляем! Вы снова являетесь подписчиком GPT-4 Access Plus"
    else:
        new_end_date = current_end_date + relativedelta(months=period)
        msg = "Поздравляем! Вы продлили подписку на GPT-4 Access Plus"

    return msg, new_end_date


async def success(user_id, period):
    months_word = await month_declination(period)

    conn = await create_connection()
    msg, new_end_date = await subscription_status(user_id, period, conn)

    await conn.execute("UPDATE user_subscriptions SET subscription_end_date = $1 WHERE user_id = $2", new_end_date, user_id)

    await bot.send_message(chat_id=user_id, text=f"{msg} на {period} {months_word}! Вам открыт VIP чат💎 и нужно общаться именно в нем")
    await bot.send_sticker(chat_id=user_id, sticker="CAACAgIAAxkBAAINqGUXHry4XQYcAYA6klTCAS0n09bUAAJeEgAC7JkpSXzv2aVH92Q7MAQ")

async def processing(user_id):
    await bot.send_message(chat_id=user_id, text="Ваш платеж в обработке")

async def fail(user_id):
    await bot.send_message(chat_id=user_id, text="Произошла ошибка, повторите попытку или обратитесь к поддержке")
