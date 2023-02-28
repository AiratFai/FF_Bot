from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.filters.state import State, StatesGroup
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


async def start_income(message: types.Message, state: FSMContext):
    """Начало диалога загрузки нового дохода"""
    text = 'Выбери категорию доходов'
    await message.reply(text, reply_markup=in_cat_kb)
    await state.set_state(FSMIncome.in_category)


async def step1(message: types.Message, state: FSMContext):
    """Ловим ответ 1"""
    await state.update_data(in_category=message.text)
    await message.reply('Введи название и сумму', reply_markup=cancel_kb)
    await state.set_state(FSMIncome.income_amount)


async def step2(message: types.Message, state: FSMContext):
    """Ловим ответ 2, добавляем запись в базу данных"""
    await state.update_data(income_amount=int(message.text.split()[-1]))
    await state.update_data(inc_name=' '.join(message.text.split()[:-1]))
    data = await state.get_data()
    await insert_income(data)
    await message.reply('Запись успешно добавлена')
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)
    await state.clear()


def register_income_handlers(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.message.register(add_income, F.text == 'Доходы')
    dp.message.register(start_income, Text(text='Добавить доход'))
    dp.message.register(step1, FSMIncome.in_category)
    dp.message.register(step2, FSMIncome.income_amount)
