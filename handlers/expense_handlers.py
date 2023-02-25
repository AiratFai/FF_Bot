from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
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


@authentication
async def start_expense(message: types.Message):
    """Начало диалога загрузки нового расхода"""
    await FSMExpense.exp_category.set()
    text = 'Выбери категорию расходов'
    await message.reply(text, reply_markup=cat_kb)


async def step1(message: types.Message, state: FSMContext):
    """Ловим ответ 1"""
    async with state.proxy() as data:
        data['exp_category'] = message.text
    await FSMExpense.next()
    await message.reply('Введи название и сумму', reply_markup=cancel_kb)


async def step2(message: types.Message, state: FSMContext):
    """Ловим ответ 2, добавляем запись в базу данных"""
    async with state.proxy() as data:
        data['exp_amount'] = int(message.text.split()[-1])
        data['exp_name'] = ' '.join(message.text.split()[:-1])
    await insert_expense(state)
    await message.reply('Запись успешно добавлена')
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)

    await state.finish()


def register_expense_handlers(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.register_message_handler(add_expense, regexp='Расходы')
    dp.register_message_handler(start_expense, regexp='Добавить расход', state=None)
    dp.register_message_handler(step1, state=FSMExpense.exp_category)
    dp.register_message_handler(step2, state=FSMExpense.exp_amount)
