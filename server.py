"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from fake_useragent import UserAgent
from data_crypto import data_crypto
from result import Result


logging.basicConfig(level=logging.INFO)
API_TOKEN = "API_TOKEN"
bot = Bot(token=API_TOKEN, parse_mode=None)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["BTC", "ETH", "XRP", "DASH", "BNB", "LUNA", "SOL", "LTC", "DOGE", "FTM", "ADA", "ATOM", "MATIC", "RUNE", "NEAR", "LINK", "ALICE", "MANA", "XTZ", "AVAX", "TRX", "YFI", "1INCH", "AUDIO", "RUB", "OMG", "1000SHIB", "NEO", "UNI", "KSM" ]
    keyboard.add(*buttons)
    await message.answer("HI BRO!",
        reply_markup=keyboard)
    

@dp.message_handler()
async def get_currency(message: types.Message):
    """Отправляет пользователю котировки"""
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, "typing")
    """Получаем список котировок лимитных ордеров"""
    data = await data_crypto(message["text"])
    """Передаем полученный список на обработку"""
    dat = Result(data)
    """Получаем биды\аски"""
    bids = dat.get_bids()
    asks = dat.get_asks()
    await message.answer(f"Цена ---- > Количество")
    """Вывод пользователю"""
    for bid in bids:
        await message.answer(bid)
    for ask in asks:
        await message.answer(ask)


if __name__ == '__main__':
    
    executor.start_polling(dp)