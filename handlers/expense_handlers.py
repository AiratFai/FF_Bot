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
    await message.reply('Введи сумму и название', reply_markup=cancel_kb)
    await state.set_state(FSMExpense.exp_amount)


async def step2(message: types.Message, state: FSMContext):
    """Ловим ответ 2, добавляем запись в базу данных"""
    await state.update_data(exp_amount=int(message.text.split()[0]))
    await state.update_data(exp_name=' '.join(message.text.split()[1:]))
    data = await state.get_data()
    await insert_expense(data)
    await message.reply('Запись успешно добавлена')
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)
    await state.clear()


async def wrong_input_1(message: types.Message, state: FSMContext):
    """Ловим ошибку ввода"""
    await message.reply(f'Нужно сначала ввести сумму, и потом через пробел название.\n'
                        f'Пример ввода: 350 Любимая колбаска', reply_markup=cancel_kb)
    await state.set_state(FSMExpense.exp_amount)


async def wrong_input_2(message: types.Message, state: FSMContext):
    """Ловим ошибку ввода"""
    await message.reply(f'Вы не ввели название расхода.\n'
                        f'Пример ввода:350 Любимая колбаска', reply_markup=cancel_kb)
    await state.set_state(FSMExpense.exp_amount)


async def wrong_input_3(message: types.Message, state: FSMContext):
    """Ловим ошибку ввода"""
    await message.reply(f'Вы не ввели сумму расхода.\n'
                        f'Пример ввода:350 Любимая сасисочка', reply_markup=cancel_kb)
    await state.set_state(FSMExpense.exp_amount)


def register_expense_handlers(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.message.register(add_expense, F.text == 'Расходы')
    dp.message.register(start_expense, Text(text='Добавить расход'))
    dp.message.register(step1, StateFilter(FSMExpense.exp_category))
    dp.message.register(wrong_input_2, StateFilter(FSMExpense.exp_amount),
                        lambda x: len(x.text.split()) == 1 and x.text.split()[0].isdigit())
    dp.message.register(wrong_input_3, StateFilter(FSMExpense.exp_amount),
                        lambda x: len(x.text.split()) == 1 and not x.text.split()[0].isdigit())
    dp.message.register(wrong_input_1, StateFilter(FSMExpense.exp_amount), lambda x: not x.text.split()[0].isdigit())
    dp.message.register(step2, StateFilter(FSMExpense.exp_amount), lambda x: x.text.split()[0].isdigit())
