import json
from datetime import datetime
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '1799874715:AAE0Rj4-SpV-OMAxLZg3hhbKIIueYwXZ9oM'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

tips_today = InlineKeyboardButton('Прогнозы на сегодня!', callback_data='tips_today')
tips_tommorow = InlineKeyboardButton('Прогнозы на завтра!', callback_data='tips_tommorow')
tips_all = InlineKeyboardButton('Все что есть!', callback_data='tips_all')
kb_date = InlineKeyboardMarkup().add(tips_today, tips_tommorow, tips_all)

tip_one = InlineKeyboardButton('Один прогноз!', callback_data='one')
tip_all = InlineKeyboardButton('Давай все!', callback_data='all')
kb_numb = InlineKeyboardMarkup().add(tip_one, tip_all)


def get_tip(day='today', count = 'one'):
    with open('bets.json', 'r') as f:
        data = json.load(f)
    if day == 'all':
        return data
    if day == 'today':
        tips = [item for item in data if item['date'].split('/')[1].split(' ')[0] == str(datetime.now().day)]
        print(tips)
        return tips
    if day == 'tomorrow':
        tips = [item for item in data if item['date'].split('/')[1].split(' ')[0] == str(datetime.now().day + 1)]
        print(tips)
        return tips


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, text="Привет. Я подберу для тебя лучшие прогнозы на спорт.", reply_markup=kb_date)


@dp.callback_query_handler(lambda c: c.data == 'tips_today')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'На сегодня!')

    tips = get_tip(day='today')
    for tip in tips:
        msg = f'----Прогноз:----\n' \
              f'Матч: {tip["title"]}\n' \
              f'Дата: {tip["date"]}\n' \
              f'Ставка: {tip["bet"]}\n' \
              f'Коэф: {tip["kf"]}\n'
        await bot.send_message(callback_query.from_user.id, msg)


@dp.callback_query_handler(lambda c: c.data == 'tips_tommorow')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'На завтра', reply_markup=kb_numb)


@dp.callback_query_handler(lambda c: c.data == 'tips_all')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Все')
    tips = get_tip(day='all')
    for tip in tips:
        msg = f'----Прогноз:----\n' \
              f'Матч: {tip["title"]}\n' \
              f'Дата: {tip["date"]}\n' \
              f'Ставка: {tip["bet"]}\n' \
              f'Коэф: {tip["kf"]}\n'
        await bot.send_message(callback_query.from_user.id, msg)


@dp.callback_query_handler(lambda c: c.data == 'one')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вот тебе один прогноз')


@dp.callback_query_handler(lambda c: c.data == 'all')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вот тебе все прогнозы')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)