from sqlalchemy import create_engine, select, func, desc
from sqlalchemy.orm import sessionmaker
from database.models import Base, MainTable, ExpenseCategories, IncomeCategories
from datetime import datetime
from settings.config import load_config

config = load_config()
url = f'{config.db.database}://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.db_user}'
engine = create_engine(url, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


async def get_num():
    """Генерирует правильный порядковый номер для записи в бд"""
    if list(session.scalars(select(MainTable.id))):
        last_id = max(list(session.scalars(select(MainTable.id))))
        last_rec = session.query(MainTable).get(last_id)
        _num = last_rec.num + 1
        return _num
    return 1


exist = session.query(IncomeCategories.id)
if len([i for i in exist]) < 2:
    for category1 in ['Продукты', 'Коммуналка', 'Авто', 'Заправка', 'Быт_химия', 'Дом', 'Развлечения', 'Здоровье',
                      'Одежда',
                      'Дети', 'Прочее']:
        session.add(ExpenseCategories(category_name=category1))
    for cat in ['Зарплата', 'Прочее']:
        session.add(IncomeCategories(category_name=cat))
    session.commit()

in_cat = {'Зарплата': 1, 'Прочее': 2}
exp_cat = {'Продукты': 1, 'Коммуналка': 2, 'Авто': 3, 'Заправка': 4, 'Быт_химия': 5, 'Дом': 6, 'Развлечения': 7,
           'Здоровье': 8, 'Одежда': 9, 'Дети': 10, 'Прочее': 11}
dates = {'Текущий месяц': (datetime.now().month, 'month'), 'Текущий год': (datetime.now().year, 'year')}


async def update_balance(sign: str):
    """Обновляет поле balance в бд после каждой записи.
     Вместо триггера, с которым я не смог разобраться"""
    max_num = max(list(session.scalars(select(MainTable.num))))
    last_id = session.query(MainTable.id).filter(MainTable.num == max_num).first()
    last = session.query(MainTable).get(last_id[0])
    prev_id = session.query(MainTable.id).filter(MainTable.num == max_num - 1).first()
    if prev_id is None:
        last.balance = last.income
    else:
        prev = session.query(MainTable).get(prev_id[0])
        if sign == '+':
            last.balance = prev.balance + last.income
        elif sign == '-':
            last.balance = prev.balance - last.expense
    session.add(last)
    session.commit()


async def insert_income(data):
    """Добавляет запись в бд"""
    m1 = MainTable(num=await get_num(),
                   income_cat_id=in_cat[data.get('in_category')],
                   name=data.get('inc_name'),
                   income=data.get('income_amount'))
    session.add(m1)
    session.commit()
    await update_balance('+')


async def insert_expense(data):
    """Добавляет запись в бд"""
    m2 = MainTable(num=await get_num(),
                   expense_cat_id=exp_cat[data.get('exp_category')],
                   name=data.get('exp_name'),
                   expense=data.get('exp_amount'))
    session.add(m2)
    session.commit()
    await update_balance('-')


async def delete_row():
    """Удаляет последнюю запись из бд"""
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


async def get_income_report(data):
    category = in_cat[data.get('rep_category')]
    date = dates[data.get('rep_period')]
    s = session.query(MainTable.date, MainTable.income).filter(MainTable.income_cat_id == category,
                                                               func.date_part(date[1], MainTable.date) == date[0]).all()
    return s


async def get_expense_report(data):
    category = exp_cat[data.get('exp_category')]
    date = dates[data.get('rep_period')]
    s = session.query(MainTable.expense).filter(MainTable.expense_cat_id == category,
                                                func.date_part(date[1], MainTable.date) == date[0]).all()
    return s


async def get_all_table(lim: int = None):
    if lim is None:
        s = session.query(MainTable).filter(func.date_part('year', MainTable.date) == datetime.now().year).order_by(
            desc(MainTable.date)).all()
    else:
        s = session.query(MainTable).filter(func.date_part('year', MainTable.date) == datetime.now().year).order_by(
            desc(MainTable.date)).limit(lim).all()
    return s

#################################################################################################################
