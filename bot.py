from create_bot import dp, bot
from handlers import general_handlers, income_handlers, expense_handlers, report_handlers


async def on_startup(_):
    print('Бот вышел в онлайн')


general_handlers.register_general_handlers(dp)
income_handlers.register_income_handlers(dp)
expense_handlers.register_expense_handlers(dp)
report_handlers.register_report_handlers(dp)

if __name__ == '__main__':
    dp.run_polling(bot)
