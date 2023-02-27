from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

"""Здесь находятся все кнопки для взаимодействия с ботом."""
b1 = KeyboardButton(text='Отмена')
cancel_kb = ReplyKeyboardMarkup(keyboard=[[b1]], resize_keyboard=True)

s_btn1 = KeyboardButton(text='Доходы')
s_btn2 = KeyboardButton(text='Расходы')
s_btn3 = KeyboardButton(text='Отчеты')
start_kb = ReplyKeyboardMarkup(keyboard=[[s_btn1, s_btn2, s_btn3]], resize_keyboard=True)

i_btn1 = KeyboardButton(text='Добавить доход')
i_btn2 = KeyboardButton(text='Удалить доход')
income_kb = ReplyKeyboardMarkup(keyboard=[[i_btn1, i_btn2]], resize_keyboard=True)

ic_btn1 = KeyboardButton(text='Зарплата')
ic_btn2 = KeyboardButton(text='Прочее')
ic_btn3 = KeyboardButton(text='Отмена')
in_cat_kb = ReplyKeyboardMarkup(keyboard=[[ic_btn1, ic_btn2, ic_btn3]], resize_keyboard=True)

e_btn1 = KeyboardButton(text='Добавить расход')
e_btn2 = KeyboardButton(text='Удалить расход')
expense_kb = ReplyKeyboardMarkup(keyboard=[[e_btn1, e_btn2]], resize_keyboard=True)

ec_btn1 = KeyboardButton(text='Продукты')
ec_btn2 = KeyboardButton(text='Коммуналка')
ec_btn3 = KeyboardButton(text='Авто')
ec_btn4 = KeyboardButton(text='Заправка')
ec_btn5 = KeyboardButton(text='Быт_химия')
ec_btn6 = KeyboardButton(text='Дом')
ec_btn7 = KeyboardButton(text='Развлечения')
ec_btn8 = KeyboardButton(text='Здоровье')
ec_btn9 = KeyboardButton(text='Одежда')
ec_btn10 = KeyboardButton(text='Айзиля')
ec_btn11 = KeyboardButton(text='Прочее')
ec_btn12 = KeyboardButton(text='Отмена')
cat_kb = ReplyKeyboardMarkup(
    keyboard=[[ec_btn1, ec_btn2, ec_btn3, ec_btn4, ec_btn5, ec_btn6, ec_btn7, ec_btn8, ec_btn9, ec_btn10, ec_btn11,
               ec_btn12]], resize_keyboard=True)

r_btn1 = KeyboardButton(text='Текущий остаток')
r_btn2 = KeyboardButton(text='Отчеты по доходам')
r_btn3 = KeyboardButton(text='Отчеты по расходам')
r_btn4 = KeyboardButton(text='Полный отчет')
report_kb = ReplyKeyboardMarkup(keyboard=[[r_btn1, r_btn2, r_btn3, r_btn4]], resize_keyboard=True)

rc_btn1 = KeyboardButton(text='Текущий месяц')
rc_btn2 = KeyboardButton(text='Текущий год')
report_cat_kb = ReplyKeyboardMarkup(keyboard=[[rc_btn1, rc_btn2]], resize_keyboard=True)

btn1 = KeyboardButton(text='Продолжить')
btn2 = KeyboardButton(text='Выход')
exit_kb = ReplyKeyboardMarkup(keyboard=[[btn1, btn2]], resize_keyboard=True)
