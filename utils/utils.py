from collections import defaultdict
from database import orm

month_names = {1: 'Январь',
               2: 'Февраль',
               3: 'Март',
               4: 'Апрель',
               5: 'Май',
               6: 'Июнь',
               7: 'Июль',
               8: 'Август',
               9: 'Сентябрь',
               10: 'Октябрь',
               11: 'Ноябрь',
               12: 'Декабрь'}


async def create_income_report_text(data, query_res):
    text = ''
    if data.get('rep_period') == 'Текущий месяц':
        income = sum([tup[1] for tup in query_res])
        text = f"Доходы за {data['rep_period'].lower()} составили <b>{income:,}</b> рублей."
    if data.get('rep_period') == 'Текущий год':
        year_income = sum([tup[1] for tup in query_res])
        od = defaultdict(int)
        for inc in query_res:
            od[inc[0].month] += inc[1]
        text = f"Доходы за {data['rep_period'].lower()} -- <b>{year_income:,}</b> рублей.\n" \
               f"{'-' * 60}\n" \
               f"Доходы по месяцам:\n"
        for k, v in od.items():
            text += f"{month_names[k]} -- <b>{v:,}</b> рублей\n"
    return text


async def create_table_text(query_res):
    table = f"|{'Дата'.center(8, ' ')}|{'Название'.center(15, ' ')}|{'+/-'.center(7, ' ')}|" \
            f"{'Остаток'.center(7, ' ')}|\n" \
            f"{'-' * 60}\n"
    for i in query_res:
        table += f"|{i.date.strftime('%d.%m.%y')}|{i.name.center(15, ' ')}|" \
                 f"{('-' + str(i.expense)).ljust(7, ' ') if i.expense else ('+' + str(i.income)).ljust(7, ' ')}|" \
                 f"{str(i.balance).ljust(7, ' ')}|\n"
    return table


async def create_expense_report_text(data):
    text = ''
    if data.get('rep_period') == 'Текущий месяц':
        query_res = await orm.get_expense_report(data)
        expense = sum([tup[0] for tup in query_res])
        text = f"Расходы за {data['rep_period'].lower()} составили <b>{expense:,}</b> рублей."
    if data.get('rep_period') == 'Текущий год':
        query_res = await orm.get_all_table()
        res = {'all_expense': 0, 'Продукты': 0, 'Коммуналка': 0, 'Авто': 0, 'Заправка': 0, 'Быт_химия': 0,
               'Дом': 0, 'Развлечения': 0, 'Здоровье': 0, 'Одежда': 0, 'Дети': 0, 'Прочее': 0}
        for i in query_res:
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
                    res['Дети'] = res.get('Дети', 0) + i.expense
                case 11:
                    res['Прочее'] = res.get('Прочее', 0) + i.expense
        text = f"Все расходы за текущий год -- {res['all_expense']} руб.\n" \
               f"{'-' * 60}\n" \
               f"Расходы по категориям:\n" \
               f"Продукты -- {res['Продукты']} руб.\n" \
               f"Коммуналка -- {res['Коммуналка']} руб.\n" \
               f"Авто -- {res['Авто']} руб.\n" \
               f"Заправка -- {res['Заправка']} руб.\n" \
               f"Быт_химия -- {res['Быт_химия']} руб.\n" \
               f"Дом -- {res['Дом']} руб.\n" \
               f"Развлечения -- {res['Развлечения']} руб.\n" \
               f"Здоровье -- {res['Здоровье']} руб.\n" \
               f"Одежда -- {res['Одежда']} руб.\n" \
               f"Дети -- {res['Дети']} руб.\n" \
               f"Прочее -- {res['Прочее']} руб.\n"
    return text
