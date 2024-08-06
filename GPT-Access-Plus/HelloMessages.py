from Config import bot, UserState, get_language, get_translation
from Keyboards import menu_kb, prechat_kb, customization_kb, about_kb, usage_kb, chat_kb, style_kb, information_kb, profile_kb, payment_kb


async def menu(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Menu", "menu")
    kb = menu_kb(language_code)
    await UserState.menu.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def prechat(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "PreChat", "prechat")
    kb = prechat_kb(language_code)
    await UserState.prechat.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def customization(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Customization", "customization")
    kb = customization_kb(language_code)
    await UserState.customization.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def about(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "About", "about")
    kb = about_kb(language_code)
    await UserState.about.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def usage(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Usage", "usage")
    kb = usage_kb(language_code)
    await UserState.usage.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def chatfree(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "ChatFree", "chatfree")
    kb = chat_kb(language_code)
    await UserState.chatfree.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def chatvip(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "ChatVIP", "chatvip")
    kb = chat_kb(language_code)
    await UserState.chatvip.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def style(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Style", "style")
    kb = style_kb(language_code)
    await UserState.style.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def information(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Information", "information")
    kb = information_kb(language_code)
    await UserState.information.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def profile(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Profile", "profile")
    kb = profile_kb(language_code)
    await UserState.profile.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def payment(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Payment", "payment")
    kb = payment_kb(language_code)
    await UserState.payment.set()
    await bot.send_message(chat_id, text, reply_markup=kb)