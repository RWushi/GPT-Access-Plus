from aiogram.types import Message, PreCheckoutQuery, LabeledPrice
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from Config import dp, bot, UserState, get_language, get_translation, wait, DB, create_connection
from HelloMessages import usage
from Keyboards import payment_kb


async def send_invoice(chat_id, description, amount, rate):
    prices = [LabeledPrice(label='Подписка GPT-4 Access Plus', amount=amount*100)]
    await bot.send_invoice(
        chat_id,
        title='Доступ к GPT-4 Access Plus',
        description=description,
        provider_token='5717382967:LIVE:638328168668588338',
        currency='kzt',
        photo_url='https://i.imgur.com/pN7JWw8.jpg',
        prices=prices,
        start_parameter='gpt4_access_plus',
        payload=f'>{rate}',
        suggested_tip_amounts=[2380*100],
        max_tip_amount=1000000*100
    )

@dp.pre_checkout_query_handler(lambda query: True, state=UserState.payment)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT, state=UserState.payment)
async def successful_payment(message: types.Message):
    rate = message.successful_payment.invoice_payload[1:]
    if rate == '1':
        add_months = 1
        months_word = "месяц"
    elif rate == '3':
        add_months = 3
        months_word = "месяца"
    elif rate == '6':
        add_months = 6
        months_word = "месяцев"
    elif rate == '12':
        add_months = 12
        months_word = "месяцев"
    else:
        add_months = 0

    user_id = message.from_user.id

    conn = await create_connection()
    current_end_date = await conn.fetchval('SELECT subscription_end_date FROM user_subscriptions WHERE user_id = $1', user_id)
    now_utc = datetime.now(timezone.utc)

    if current_end_date is None:
        new_end_date = now_utc + relativedelta(months=add_months)
        msg = "Поздравляем! Теперь Вы являетесь подписчиком GPT-4 Access Plus"
    elif current_end_date < now_utc:
        new_end_date = now_utc + relativedelta(months=add_months)
        msg = "Поздравляем! Вы снова являетесь подписчиком GPT-4 Access Plus"
    else:
        new_end_date = current_end_date + relativedelta(months=add_months)
        msg = "Поздравляем! Вы продлили подписку на GPT-4 Access Plus"

    await conn.execute("UPDATE user_subscriptions SET subscription_end_date = $1 WHERE user_id = $2", new_end_date, user_id)
    await conn.close()

    await bot.send_message(chat_id=message.chat.id, text=f"{msg} на {add_months} {months_word}! Вам открыт VIP чат💎 и нужно общаться именно в нем")
    await bot.send_sticker(chat_id=message.chat.id, sticker="CAACAgIAAxkBAAINqGUXHry4XQYcAYA6klTCAS0n09bUAAJeEgAC7JkpSXzv2aVH92Q7MAQ")


@dp.message_handler(state=UserState.payment)
async def payment_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "Payment", "1_month"):
        await message.answer(wait)
        await send_invoice(chat_id, 'Подписка на 1 месяц', 7080, 1)

    elif message.text == get_translation(language_code, "Payment", "3_months"):
        await message.answer(wait)
        await send_invoice(chat_id, 'Подписка на 3 месяца', 18880, 3)

    elif message.text == get_translation(language_code, "Payment", "6_months"):
        await message.answer(wait)
        await send_invoice(chat_id, 'Подписка на 6 месяцев', 33040, 6)

    elif message.text == get_translation(language_code, "Payment", "12_months"):
        await message.answer(wait)
        await send_invoice(chat_id, 'Подписка на 12 месяцев', 56640, 12)

    elif message.text == get_translation(language_code, "Common", "return_back"):
        await message.answer(wait)
        await usage(message.chat.id)