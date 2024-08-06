from aiogram.types import Message
from Config import dp, UserState, get_translation, wait
from ChatDB import pre_check_free, pre_check_vip
from HelloMessages import menu, chatfree, chatvip
import ChatFree, ChatVIP


@dp.message_handler(state=UserState.prechat)
async def prechat_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "PreChat", "free_chat"):
        await message.answer(wait)
        if await pre_check_free(message.from_user.id):
            await chatfree(chat_id)
        else:
            pass

    elif message.text == get_translation(language_code, "PreChat", "vip_chat"):
        await message.answer(wait)
        if await pre_check_vip(message.from_user.id):
            await chatvip(chat_id)
        else:
            pass

    elif message.text == get_translation(language_code, "Subcommon", "what_is_difference"):
        await message.answer(get_translation(language_code, "PreChat", "difference"))

    elif message.text == get_translation(language_code, "Common", "return_menu"):
        await message.answer(wait)
        await menu(chat_id)