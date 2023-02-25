from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

"""Здесь находятся все кнопки для взаимодействия с ботом."""

cancel_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
b1 = KeyboardButton('Отмена')
cancel_kb.add(b1)

start_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
s_btn1 = KeyboardButton('Доходы')
s_btn2 = KeyboardButton('Расходы')
s_btn3 = KeyboardButton('Отчеты')
start_kb.add(s_btn1, s_btn2, s_btn3)

income_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
i_btn1 = KeyboardButton('Добавить доход')
i_btn2 = KeyboardButton('Удалить доход')
income_kb.add(i_btn1, i_btn2)

in_cat_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
ic_btn1 = KeyboardButton('Зарплата')
ic_btn2 = KeyboardButton('Прочее')
ic_btn3 = KeyboardButton('Отмена')
in_cat_kb.add(ic_btn1, ic_btn2, ic_btn3)

expense_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
e_btn1 = KeyboardButton('Добавить расход')
e_btn2 = KeyboardButton('Удалить расход')
expense_kb.add(e_btn1, e_btn2)

cat_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
ec_btn1 = KeyboardButton('Продукты')
ec_btn2 = KeyboardButton('Коммуналка')
ec_btn3 = KeyboardButton('Авто')
ec_btn4 = KeyboardButton('Заправка')
ec_btn5 = KeyboardButton('Быт_химия')
ec_btn6 = KeyboardButton('Дом')
ec_btn7 = KeyboardButton('Развлечения')
ec_btn8 = KeyboardButton('Здоровье')
ec_btn9 = KeyboardButton('Одежда')
ec_btn10 = KeyboardButton('Айзиля')
ec_btn11 = KeyboardButton('Прочее')
ec_btn12 = KeyboardButton('Отмена')
cat_kb.row(ec_btn1, ec_btn2, ec_btn3).row(ec_btn4, ec_btn5, ec_btn6).row(ec_btn7, ec_btn8, ec_btn9).row(ec_btn10,
                                                                                                        ec_btn11,
                                                                                                        ec_btn12)
report_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
r_btn1 = KeyboardButton('Текущий остаток')
r_btn2 = KeyboardButton('Отчеты по доходам')
r_btn3 = KeyboardButton('Отчеты по расходам')
r_btn4 = KeyboardButton('Полный отчет')
report_kb.add(r_btn1, r_btn2, r_btn3, r_btn4)

report_cat_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
rc_btn1 = KeyboardButton('Текущий месяц')
rc_btn2 = KeyboardButton('Текущий год')
report_cat_kb.add(rc_btn1, rc_btn2)

exit_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn1 = KeyboardButton('Продолжить')
btn2 = KeyboardButton('Выход')
exit_kb.add(btn1, btn2)
