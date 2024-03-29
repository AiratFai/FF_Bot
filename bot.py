import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from create_bot import bot, dp, set_main_menu
from handlers import general_handlers, income_handlers, expense_handlers, report_handlers, other_handlers

# Инициализируем логгер
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(general_handlers.reminder, 'cron', day_of_week='mon-sun', hour=19, minute=50, end_date='2025-10-13')


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    # Регистрируем хендлеры в диспетчере
    general_handlers.register_general_handlers(dp)
    income_handlers.register_income_handlers(dp)
    expense_handlers.register_expense_handlers(dp)
    report_handlers.register_report_handlers(dp)
    other_handlers.register_other_handler(dp)

    dp.startup.register(set_main_menu)
    # Пропускаем накопившиеся апдейты и запускаем polling
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        # Запускаем функцию main в асинхронном режиме
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
