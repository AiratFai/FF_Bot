from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.filters.state import State, StatesGroup
from keyboards import report_kb, cat_kb, report_cat_kb, in_cat_kb, exit_kb
from create_bot import bot, authentication
from database import orm
from utils import create_income_report_text, create_table_text, create_expense_report_text


class FSMIncomeReport(StatesGroup):
    rep_period = State()
    rep_category = State()


class FSMIExpenseReport(StatesGroup):
    exp_rep_period = State()
    exp_rep_category = State()


@authentication
async def start_report(message: types.Message):
    """Начало диалога загрузки нового отчета"""
    text = 'Выбери тип отчета'
    await message.reply(text, reply_markup=report_kb)


async def get_current_balance(message: types.Message):
    """Узнать текущий остаток"""
    data, balance = await orm.get_balance_report()
    await message.reply(f'Остаток на {data} составляет <b>{balance:,}</b> рублей')
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)


#############################################################################

async def in_step1(message: types.Message, state: FSMContext):
    """Начало диалога загрузки нового отчета"""
    text = 'Выбери период отчета'
    await message.reply(text, reply_markup=report_cat_kb)
    await state.set_state(FSMIncomeReport.rep_period)


async def in_step2(message: types.Message, state: FSMContext):
    """Ловим ответ 1"""
    await state.update_data(rep_period=message.text)
    await message.reply('Выбери категорию дохода', reply_markup=in_cat_kb)
    await state.set_state(FSMIncomeReport.rep_category)


async def in_step3(message: types.Message, state: FSMContext):
    """Ловим ответ 3"""
    await state.update_data(rep_category=message.text)
    data = await state.get_data()
    query = await orm.get_income_report(data)
    text = await create_income_report_text(data, query)
    await message.reply(text)
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)
    await state.clear()


#################################################################################

async def exp_step1(message: types.Message, state: FSMContext):
    """Начало диалога загрузки нового отчета"""
    text = 'Выбери период отчета'
    await message.reply(text, reply_markup=report_cat_kb)
    await state.set_state(FSMIExpenseReport.exp_rep_period)


async def exp_step2_1(message: types.Message, state: FSMContext):
    """Ловим ответ 1"""
    await state.update_data(rep_period=message.text)
    await message.reply('Выбери категорию расхода', reply_markup=cat_kb)
    await state.set_state(FSMIExpenseReport.exp_rep_category)


async def exp_step2_2(message: types.Message, state: FSMContext):
    """Ловим ответ 3"""
    await state.update_data(rep_period=message.text)
    data = await state.get_data()
    text = await create_expense_report_text(data)
    await message.reply(text)
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)
    await state.clear()


async def exp_step3(message: types.Message, state: FSMContext):
    """Ловим ответ 3"""
    await state.update_data(exp_category=message.text)
    data = await state.get_data()
    text = await create_expense_report_text(data)
    await message.reply(text)
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)
    await state.clear()


async def get_table(message: types.Message):
    query = await orm.get_all_table(50)
    text = await create_table_text(query)
    await bot.send_message(message.from_user.id, text)
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)


def register_report_handlers(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.message.register(start_report, Text(text='Отчеты'))
    dp.message.register(get_current_balance, Text(text='Текущий остаток'))
    dp.message.register(in_step1, Text(text='Отчеты по доходам'))
    dp.message.register(in_step2, FSMIncomeReport.rep_period)
    dp.message.register(in_step3, FSMIncomeReport.rep_category)
    dp.message.register(exp_step1, Text(text='Отчеты по расходам'))
    dp.message.register(exp_step2_1, FSMIExpenseReport.exp_rep_period, lambda x: x.text == 'Текущий месяц')
    dp.message.register(exp_step2_2, FSMIExpenseReport.exp_rep_period, lambda x: x.text == 'Текущий год')
    dp.message.register(exp_step3, FSMIExpenseReport.exp_rep_category)
    dp.message.register(get_table, Text(text='Таблица'))
