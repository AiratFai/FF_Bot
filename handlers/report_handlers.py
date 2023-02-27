from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.filters.state import State, StatesGroup
from keyboards import report_kb, cat_kb, report_cat_kb, in_cat_kb, exit_kb
from create_bot import bot, authentication
from database.orm import get_balance_report, get_income_report, get_expense_report, get_reports


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
    data, balance = await get_balance_report()
    await message.reply(f'Остаток на {data} составляет {balance:,} рублей')
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)


#############################################################################
@authentication
async def in_step1(message: types.Message):
    """Начало диалога загрузки нового отчета"""
    await FSMIncomeReport.rep_period.set()
    text = 'Выбери период отчета'
    await message.reply(text, reply_markup=report_cat_kb)


async def in_step2(message: types.Message, state: FSMContext):
    """Ловим ответ 1"""
    async with state.proxy() as data:
        data['rep_period'] = message.text
    await FSMIncomeReport.next()
    await message.reply('Выбери категорию дохода', reply_markup=in_cat_kb)


async def in_step3(message: types.Message, state: FSMContext):
    """Ловим ответ 3"""
    async with state.proxy() as data:
        data['rep_category'] = message.text
    async with state.proxy() as data:
        await message.reply(
            f"Доходы за {data['rep_period'].lower()} составили {await get_income_report(state):,} рублей.")

    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)
    await state.finish()


#################################################################################
@authentication
async def exp_step1(message: types.Message):
    """Начало диалога загрузки нового отчета"""
    await FSMIExpenseReport.exp_rep_period.set()
    text = 'Выбери период отчета'
    await message.reply(text, reply_markup=report_cat_kb)


async def exp_step2(message: types.Message, state: FSMContext):
    """Ловим ответ 1"""
    async with state.proxy() as data:
        data['rep_period'] = message.text
    await FSMIExpenseReport.next()
    await message.reply('Выбери категорию расхода', reply_markup=cat_kb)


async def exp_step3(message: types.Message, state: FSMContext):
    """Ловим ответ 3"""
    async with state.proxy() as data:
        data['exp_category'] = message.text
    async with state.proxy() as data:
        await message.reply(
            f"Расходы за {data['rep_period'].lower()} составили {await get_expense_report(state):,} рублей.")

    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)
    await state.finish()


async def get_all_reports(message: types.Message):
    d = get_reports()
    text = f"Все доходы за текущий год -- {d['all_income']} руб.\n" \
           f"Все расходы за текущий год -- {d['all_expense']} руб.\n" \
           f"Расходы по категориям:\n" \
           f"Продукты -- {d['Продукты']} руб.\n" \
           f"Коммуналка -- {d['Коммуналка']} руб.\n" \
           f"Авто -- {d['Авто']} руб.\n" \
           f"Заправка -- {d['Заправка']} руб.\n" \
           f"Быт_химия -- {d['Быт_химия']} руб.\n" \
           f"Дом -- {d['Дом']} руб.\n" \
           f"Развлечения -- {d['Развлечения']} руб.\n" \
           f"Здоровье -- {d['Здоровье']} руб.\n" \
           f"Одежда -- {d['Одежда']} руб.\n" \
           f"Айзиля -- {d['Айзиля']} руб.\n" \
           f"Прочее -- {d['Прочее']} руб.\n"
    await bot.send_message(message.from_user.id, text)
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)


def register_report_handlers(dp: Dispatcher):
    """Регистрируем хендлеры"""
    dp.message.register(start_report, Text(text='Отчеты'))
    dp.message.register(get_current_balance, Text(text='Текущий остаток'))
    dp.message.register(in_step1, Text(text='Отчеты по доходам'))
    # dp.message.register(in_step2, state=FSMIncomeReport.rep_period)
    # dp.message.register(in_step3, state=FSMIncomeReport.rep_category)
    dp.message.register(exp_step1, Text(text='Отчеты по расходам'))
    # dp.message.register(exp_step2, state=FSMIExpenseReport.exp_rep_period)
    # dp.message.register(exp_step3, state=FSMIExpenseReport.exp_rep_category)
    dp.message.register(get_all_reports, Text(text='Полный отчет'))
