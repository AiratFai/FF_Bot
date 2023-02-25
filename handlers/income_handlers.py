from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, authentication
from keyboards import income_kb, in_cat_kb, cancel_kb, exit_kb
from database.orm import insert_income


class FSMIncome(StatesGroup):
    in_category = State()
    income_amount = State()


@authentication
async def add_income(message: types.Message):
    text = 'Что ты хочешь сделать?'
    await bot.send_message(message.from_user.id, text, reply_markup=income_kb)


@authentication
async def start_income(message: types.Message):
    """Начало диалога загрузки нового дохода"""
    await FSMIncome.in_category.set()
    text = 'Выбери категорию доходов'
    await message.reply(text, reply_markup=in_cat_kb)


async def step1(message: types.Message, state: FSMContext):
    """Ловим ответ 1"""
    async with state.proxy() as data:
        data['in_category'] = message.text
    await FSMIncome.next()
    await message.reply('Введи название и сумму', reply_markup=cancel_kb)


async def step2(message: types.Message, state: FSMContext):
    """Ловим ответ 2, добавляем запись в базу данных"""
    async with state.proxy() as data:
        data['income_amount'] = int(message.text.split()[-1])
        data['inc_name'] = ' '.join(message.text.split()[:-1])
    await insert_income(state)
    await message.reply('Запись успешно добавлена')
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)

    await state.finish()


def register_income_handlers(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.register_message_handler(add_income, regexp='Доходы')
    dp.register_message_handler(start_income, regexp='Добавить доход', state=None)
    dp.register_message_handler(step1, state=FSMIncome.in_category)
    dp.register_message_handler(step2, state=FSMIncome.income_amount)
