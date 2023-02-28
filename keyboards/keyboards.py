from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

"""Здесь находятся все кнопки для взаимодействия с ботом."""
b1 = KeyboardButton(text='Отмена')
cancel_kb = ReplyKeyboardMarkup(keyboard=[[b1]], resize_keyboard=True)

start_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=word) for word in ['Доходы', 'Расходы', 'Отчеты']]],
                               resize_keyboard=True)

income_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=word) for word in ['Добавить доход', 'Удалить доход']]],
                                resize_keyboard=True)

in_cat_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=word) for word in ['Зарплата', 'Прочее', 'Отмена']]],
                                resize_keyboard=True)

expense_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=word) for word in ['Добавить расход', 'Удалить расход']]], resize_keyboard=True)

words = [['Продукты', 'Коммуналка', 'Авто'],
         ['Заправка', 'Быт_химия', 'Дом'],
         ['Развлечения', 'Здоровье', 'Одежда'],
         ['Айзиля', 'Прочее', 'Отмена']]
keyboard = [[KeyboardButton(text=words[j][i]) for i in range(3)] for j in range(4)]
cat_kb = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

report_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=word)] for word in
                                          ['Текущий остаток', 'Отчеты по доходам', 'Отчеты по расходам',
                                           'Полный отчет']], resize_keyboard=True)

report_cat_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=word) for word in ['Текущий месяц', 'Текущий год']]],
                                    resize_keyboard=True)

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=word) for word in ['Продолжить', 'Выход']]],
                              resize_keyboard=True)
