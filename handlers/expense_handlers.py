from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.filters.state import State, StatesGroup
from create_bot import bot, authentication
from keyboards import expense_kb, cat_kb, cancel_kb, exit_kb
from database.orm import insert_expense


class FSMExpense(StatesGroup):
    exp_category = State()
    exp_amount = State()


@authentication
async def add_expense(message: types.Message):
    text = 'Что ты хочешь сделать?'
    await bot.send_message(message.from_user.id, text, reply_markup=expense_kb)


async def start_expense(message: types.Message, state: FSMContext):
    """Начало диалога загрузки нового расхода"""
    text = 'Выбери категорию расходов'
    await message.reply(text, reply_markup=cat_kb)
    await state.set_state(FSMExpense.exp_category)


async def step1(message: types.Message, state: FSMContext):
    """Ловим ответ 1"""
    await state.update_data(exp_category=message.text)
    await message.reply('Введи название и сумму', reply_markup=cancel_kb)
    await state.set_state(FSMExpense.exp_amount)


async def step2(message: types.Message, state: FSMContext):
    """Ловим ответ 2, добавляем запись в базу данных"""
    await state.update_data(exp_amount=int(message.text.split()[-1]))
    await state.update_data(exp_name=' '.join(message.text.split()[:-1]))
    data = await state.get_data()
    await insert_expense(data)
    await message.reply('Запись успешно добавлена')
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)
    await state.clear()


def register_expense_handlers(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.message.register(add_expense, F.text == 'Расходы')
    dp.message.register(start_expense, Text(text='Добавить расход'))
    dp.message.register(step1, FSMExpense.exp_category)
    dp.message.register(step2, FSMExpense.exp_amount)
