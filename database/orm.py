from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from database.models import Base, MainTable, ExpenseCategories, IncomeCategories
from datetime import datetime
from settings import db_config

engine = create_engine(db_config.url, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

exist = session.query(IncomeCategories.id)
if len([i for i in exist]) < 2:
    for category1 in ['Продукты', 'Коммуналка', 'Авто', 'Заправка', 'Быт_химия', 'Дом', 'Развлечения', 'Здоровье',
                      'Одежда',
                      'Айзиля', 'Прочее']:
        session.add(ExpenseCategories(category_name=category1))
    for cat in ['Зарплата', 'Прочее']:
        session.add(IncomeCategories(category_name=cat))
    session.commit()

in_cat = {'Зарплата': 1, 'Прочее': 2}
exp_cat = {'Продукты': 1, 'Коммуналка': 2, 'Авто': 3, 'Заправка': 4, 'Быт_химия': 5, 'Дом': 6, 'Развлечения': 7,
           'Здоровье': 8, 'Одежда': 9, 'Айзиля': 10, 'Прочее': 11}
dates = {'Текущий месяц': (datetime.now().month, 'month'), 'Текущий год': (datetime.now().year, 'year')}


def update_balance(sign: str):
    max_id = max(list(session.scalars(select(MainTable.id))))
    last = session.query(MainTable).get(max_id)
    prev = session.query(MainTable).get(max_id - 1)
    if sign == '+':
        last.balance = prev.balance + last.income
    elif sign == '-':
        last.balance = prev.balance - last.expense
    session.add(last)
    session.commit()


async def insert_income(state):
    async with state.proxy() as data:
        m1 = MainTable(income_cat_id=in_cat[data.get('in_category')],
                       name=data.get('inc_name'),
                       income=data.get('income_amount'))
        session.add(m1)
        session.commit()

    update_balance('+')


async def insert_expense(state):
    async with state.proxy() as data:
        m2 = MainTable(expense_cat_id=exp_cat[data.get('exp_category')],
                       name=data.get('exp_name'),
                       expense=data.get('exp_amount'))
        session.add(m2)
        session.commit()

    update_balance('-')


async def delete_row():
    max_id = max(list(session.scalars(select(MainTable.id))))
    i = session.query(MainTable).filter(MainTable.id == max_id).one()
    session.delete(i)
    session.commit()


async def get_balance_report():
    max_id = max(list(session.scalars(select(MainTable.id))))
    s = session.query(MainTable).get(max_id)
    balance = s.balance
    data = datetime.now().strftime('%d.%m.%Y')
    return data, balance


async def get_income_report(state):
    async with state.proxy() as data:
        category = in_cat[data.get('rep_category')]
        date = dates[data.get('rep_period')]
        s = session.query(MainTable.income).filter(MainTable.income_cat_id == category,
                                                   func.date_part(date[1], MainTable.date) == date[0]).all()
        income = 0
        for tup in s:
            for inc in tup:
                income += inc
        return income


async def get_expense_report(state):
    async with state.proxy() as data:
        category = exp_cat[data.get('exp_category')]
        date = dates[data.get('rep_period')]
        s = session.query(MainTable.expense).filter(MainTable.expense_cat_id == category,
                                                    func.date_part(date[1], MainTable.date) == date[0]).all()
        expense = 0
        for tup in s:
            for exp in tup:
                expense += exp
        return expense


def get_reports():
    s = session.query(MainTable).filter(func.date_part('year', MainTable.date) == datetime.now().year).all()
    res = {'all_income': 0, 'all_expense': 0, 'Продукты': 0, 'Коммуналка': 0, 'Авто': 0, 'Заправка': 0, 'Быт_химия': 0,
           'Дом': 0, 'Развлечения': 0,
           'Здоровье': 0, 'Одежда': 0, 'Айзиля': 0, 'Прочее': 0}
    for i in s:
        res['all_income'] = res.get('all_income', 0) + i.income
        res['all_expense'] = res.get('all_expense', 0) + i.expense
        match i.expense_cat_id:
            case 1:
                res['Продукты'] = res.get('Продукты', 0) + i.expense
            case 2:
                res['Коммуналка'] = res.get('Коммуналка', 0) + i.expense
            case 3:
                res['Авто'] = res.get('Авто', 0) + i.expense
            case 4:
                res['Заправка'] = res.get('Заправка', 0) + i.expense
            case 5:
                res['Быт_химия'] = res.get('Быт_химия', 0) + i.expense
            case 6:
                res['Дом'] = res.get('Дом', 0) + i.expense
            case 7:
                res['Развлечения'] = res.get('Развлечения', 0) + i.expense
            case 8:
                res['Здоровье'] = res.get('Здоровье', 0) + i.expense
            case 9:
                res['Одежда'] = res.get('Одежда', 0) + i.expense
            case 10:
                res['Айзиля'] = res.get('Айзиля', 0) + i.expense
            case 11:
                res['Прочее'] = res.get('Прочее', 0) + i.expense
    return res
