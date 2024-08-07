from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from States import PostgresStateStorage
import asyncpg, json, os

wait = "⏳"

DATABASE_CONFIG = {
    'host': '',
    'database': '',
    'user': '',
    'password': '',
    'port': '5432',
    'ssl': 'require'
}

storage = PostgresStateStorage(**DATABASE_CONFIG)

async def create_connection():
    return await asyncpg.connect(**DATABASE_CONFIG)

class DB:
    async def __aenter__(self):
        self.conn = await create_connection()
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


async def add_new_user(user_id):
    async with DB() as conn:
        await conn.execute('''
            INSERT INTO user_settings (user_id, language, style, chat_history, information) 
            VALUES ($1, NULL, NULL, NULL, NULL) ON CONFLICT (user_id) DO NOTHING
        ''', user_id)

        await conn.execute('''
            INSERT INTO user_subscriptions (user_id, free_messages_left, subscription_end_date) 
            VALUES ($1, 5, NULL) ON CONFLICT (user_id) DO NOTHING
        ''', user_id)


class UserState(StatesGroup):
    language = State()
    menu = State()
    prechat = State()
    chatfree = State()
    chatvip = State()
    customization = State()
    about = State()
    usage = State()
    style = State()
    information = State()
    profile = State()
    payment = State()

bot = Bot(token='')
dp = Dispatcher(bot, storage=storage)


TRANSLATIONS = {}

def load_translations():
    for lang_file in os.listdir("translations"):
        if lang_file.endswith(".json"):
            lang_code = lang_file[:-5]
            with open(f"translations/{lang_file}", "r", encoding="utf-8") as f:
                TRANSLATIONS[lang_code] = json.load(f)

load_translations()


def get_translation(language_code, category, key):
    value = TRANSLATIONS.get(language_code, {}).get(category, {}).get(key)
    print(f"get_translation: {language_code}, {category}, {key}, value: {value}")
    return value

#def get_translation(language_code, category, key):
    #print(f"get_translation: {language_code}, {category}, {key}")
    #return TRANSLATIONS.get(language_code, {}).get(category, {}).get(key)

async def get_language(user_id):
    async with DB() as conn:
        chosen_lang = await conn.fetchval('SELECT language FROM user_settings WHERE user_id = $1', user_id)
    return chosen_lang

class LanguageMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        chat_id = message.chat.id
        message.conf['language_code'] = await get_language(chat_id)

dp.middleware.setup(LanguageMiddleware())


OPENAI_API_KEY = ''
