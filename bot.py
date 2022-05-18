import json
from datetime import datetime
import random
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '1799874715:AAE0Rj4-SpV-OMAxLZg3hhbKIIueYwXZ9oM'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


tip_one_today = InlineKeyboardButton('Сегодня - Один прогноз!', callback_data='one_today')
tip_all_today = InlineKeyboardButton('Сегодня - Давай все!', callback_data='all_today')
tip_one_tomorrow = InlineKeyboardButton('Завтра - Один прогноз!', callback_data='one_tomorrow')
tip_all_tomorrow = InlineKeyboardButton('Завтра - Давай все!', callback_data='all_tomorrow')
tip_all = InlineKeyboardButton('Давай все что есть!', callback_data='all')
kb = InlineKeyboardMarkup().add(tip_one_today, tip_all_today, tip_one_tomorrow, tip_all_tomorrow, tip_all)


def get_tip(day='today', count = 'one'):
    with open('bets.json', 'r') as f:
        data = json.load(f)
    if day == 'all':
        return data
    if day == 'today':
        tips = [item for item in data if item['date'].split('/')[1].split(' ')[0] == str(datetime.now().day)]
        if count == 'all':
            return tips
        if count =='one':
            return tips[random.randint(0, len(tips))]
    if day == 'tomorrow':
        tips = [item for item in data if item['date'].split('/')[1].split(' ')[0] == str(datetime.now().day + 1)]
        if count == 'all':
            return tips
        if count == 'one':
            return tips[random.randint(0, len(tips))]


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, text="Привет. Я подберу для тебя лучшие прогнозы на спорт.", reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'all')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Все')
    tips = get_tip(day='all', count='all')
    for tip in tips:
        msg = f'----Прогноз:----\n' \
              f'Матч: {tip["title"]}\n' \
              f'Дата: {tip["date"]}\n' \
              f'Ставка: {tip["bet"]}\n' \
              f'Коэф: {tip["kf"]}\n'
        await bot.send_message(callback_query.from_user.id, msg)


@dp.callback_query_handler(lambda c: c.data == 'one_today')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вот тебе один прогноз на сегодня')
    tip = get_tip(day='today', count='one')
    msg = f'---------Прогноз:--------\n' \
        f'Матч: {tip["title"]}\n' \
        f'Дата: {tip["date"]}\n' \
        f'Ставка: {tip["bet"]}\n' \
        f'Коэф: {tip["kf"]}\n'
    await bot.send_message(callback_query.from_user.id, msg)


@dp.callback_query_handler(lambda c: c.data == 'all_today')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вот тебе все прогнозы на сегодня')
    tips = get_tip(day='today', count='all')
    for tip in tips:
        msg = f'---------Прогноз:--------\n' \
              f'Матч: {tip["title"]}\n' \
              f'Дата: {tip["date"]}\n' \
              f'Ставка: {tip["bet"]}\n' \
              f'Коэф: {tip["kf"]}\n'
        await bot.send_message(callback_query.from_user.id, msg)


@dp.callback_query_handler(lambda c: c.data == 'one_tomorrow')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вот тебе один прогноз на сегодня')
    tip = get_tip(day='tomorrow', count='one')
    msg = f'---------Прогноз:--------\n' \
        f'Матч: {tip["title"]}\n' \
        f'Дата: {tip["date"]}\n' \
        f'Ставка: {tip["bet"]}\n' \
        f'Коэф: {tip["kf"]}\n'
    await bot.send_message(callback_query.from_user.id, msg)


@dp.callback_query_handler(lambda c: c.data == 'all_tomorrow')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вот тебе все прогнозы на сегодня')
    tips = get_tip(day='tomorrow', count='all')
    for tip in tips:
        msg = f'---------Прогноз:--------\n' \
              f'Матч: {tip["title"]}\n' \
              f'Дата: {tip["date"]}\n' \
              f'Ставка: {tip["bet"]}\n' \
              f'Коэф: {tip["kf"]}\n'
        await bot.send_message(callback_query.from_user.id, msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)