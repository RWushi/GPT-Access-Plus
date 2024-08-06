from aiogram.types import Message, ChatActions
from Config import dp, bot, UserState, get_translation, wait, OPENAI_API_KEY
from ChatDB import save_history, reset_history, get_user_data
from HelloMessages import prechat
import json, openai

openai.api_key = OPENAI_API_KEY

@dp.message_handler(state=UserState.chatvip)
async def chatvip_handler(message: Message):
    language_code = message.conf.get('language_code')
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "ChatCommon", "new_dialog"):
        await message.answer(wait)
        await reset_history(user_id)
        await message.answer(get_translation(language_code, "ChatVIP", "reset"))

    elif message.text == get_translation(language_code, "Common", "return_back"):
        await message.answer(wait)
        await prechat(chat_id)


@dp.message_handler(state=UserState.chatvip)
async def echo(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    await bot.send_chat_action(chat_id, ChatActions.TYPING)

    history, style, information = await get_user_data(user_id)

    if isinstance(history, str):
        history = json.loads(history)

    gpt_response_text = await gpt_response(message.text, history, style, information, user_id)

    await message.answer(gpt_response_text)


async def gpt_response(prompt, history, style, information, user_id):
    if history is None:
        history = []
    if len(history) == 0:
        system_message = "style: {}\ninformation: {}".format(style, information)
        history.append({"role": "system", "content": system_message})

    if not isinstance(history, list):
        history = []

    history.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=history,
        temperature=0.1,
        max_tokens=1000
    )

    generated_message = response['choices'][0]['message']['content'].strip()
    history.append({"role": "assistant", "content": generated_message})

    await save_history(user_id, history)

    return generated_message
