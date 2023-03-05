from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text, StateFilter
from aiogram.filters.state import State, StatesGroup
from create_bot import bot, authentication
from keyboards import expense_kb, cat_kb, cancel_kb, exit_kb
from database.orm import insert_expense


class FSMExpense(StatesGroup):
    exp_category = State()
    exp_amount = State()


@authentication
async def add_expense(message: types.Message):
    text = 'Значит все-таки потратила..'
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


async def wrong_input(message: types.Message, state: FSMContext):
    """Ловим ошибку"""
    await message.reply(f'Нужно сначала ввести название, и потом через пробел сумму.\n'
                        f'Пример ввода: Любимая колбаска 350', reply_markup=cancel_kb)
    await state.set_state(FSMExpense.exp_amount)


def register_expense_handlers(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.message.register(add_expense, F.text == 'Расходы')
    dp.message.register(start_expense, Text(text='Добавить расход'))
    dp.message.register(step1, StateFilter(FSMExpense.exp_category))
    dp.message.register(step2, StateFilter(FSMExpense.exp_amount), lambda x: x.text.split()[-1].isdigit())
    dp.message.register(wrong_input, StateFilter(FSMExpense.exp_amount), lambda x: not x.text.split()[-1].isdigit())
