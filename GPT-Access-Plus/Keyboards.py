from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from Config import get_translation

language_kb = InlineKeyboardMarkup()
english = InlineKeyboardButton("English🇺🇸", callback_data="lang:EN")
chinese = InlineKeyboardButton("中文🇨🇳", callback_data="lang:CN")
russian = InlineKeyboardButton("Русский🇷🇺", callback_data="lang:RU")
kazakh = InlineKeyboardButton("Қазақша🇰🇿", callback_data="lang:KZ")

language_kb.add(english, chinese, russian, kazakh)


def menu_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "Menu", "chat_with_gpt4"))],
            [KeyboardButton(text=get_translation(language_code, "Menu", "customization"))],
            [
                KeyboardButton(text=get_translation(language_code, "Menu", "about_bot")),
                KeyboardButton(text=get_translation(language_code, "Menu", "usage"))
            ],
            [KeyboardButton(text=get_translation(language_code, "Menu", "made_by_rtools"))]
        ],
        resize_keyboard=True
    )
    return kb

def prechat_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "PreChat", "free_chat"))],
            [KeyboardButton(text=get_translation(language_code, "PreChat", "vip_chat"))],
            [KeyboardButton(text=get_translation(language_code, "Subcommon", "what_is_difference"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_menu"))]
        ],
        resize_keyboard=True
    )
    return kb

def customization_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "Customization", "set_style"))],
            [KeyboardButton(text=get_translation(language_code, "Customization", "set_info"))],
            [KeyboardButton(text=get_translation(language_code, "Subcommon", "what_is_this"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_menu"))]
        ],
        resize_keyboard=True
    )
    return kb

def about_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "About", "about_product"))],
            [
                KeyboardButton(text=get_translation(language_code, "About", "features")),
                KeyboardButton(text=get_translation(language_code, "About", "advantages"))
            ],
            [KeyboardButton(text=get_translation(language_code, "About", "additional_info"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_menu"))]
        ],
        resize_keyboard=True
    )
    return kb

def usage_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "Usage", "my_profile"))],
            [
                KeyboardButton(text=get_translation(language_code, "Usage", "rates")),
                KeyboardButton(text=get_translation(language_code, "Usage", "payment"))
            ],
            [KeyboardButton(text=get_translation(language_code, "Usage", "support"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_menu"))]
        ],
        resize_keyboard=True
    )
    return kb

def chat_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "ChatCommon", "new_dialog"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_back"))]
        ],
        resize_keyboard=True
    )
    return kb

def style_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "SubCommon", "view_example"))],
            [KeyboardButton(text=get_translation(language_code, "Style", "current"))],
            [KeyboardButton(text=get_translation(language_code, "Style", "reset"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_back"))]
        ],
        resize_keyboard=True
    )
    return kb

def information_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "SubCommon", "view_example"))],
            [KeyboardButton(text=get_translation(language_code, "Information", "current"))],
            [KeyboardButton(text=get_translation(language_code, "Information", "reset"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_back"))]
        ],
        resize_keyboard=True
    )
    return kb

def profile_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_translation(language_code, "Profile", "trial_requests")),
                KeyboardButton(text=get_translation(language_code, "Profile", "my_subscription"))
            ],
            [KeyboardButton(text=get_translation(language_code, "Profile", "my_id"))],
            [KeyboardButton(text=get_translation(language_code, "Profile", "change_language"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_back"))]
        ],
        resize_keyboard=True
    )
    return kb

def payment_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_translation(language_code, "Payment", "1_month")),
                KeyboardButton(text=get_translation(language_code, "Payment", "3_months"))
            ],
            [
                KeyboardButton(text=get_translation(language_code, "Payment", "6_months")),
                KeyboardButton(text=get_translation(language_code, "Payment", "12_months"))
            ],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_back"))]
        ],
        resize_keyboard=True
    )
    return kb