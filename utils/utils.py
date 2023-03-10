from collections import defaultdict

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
            text += f"{month_names[k]} -- <b>{v:,}</b> рублей"
    return text
