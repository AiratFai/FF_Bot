from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from settings.config import load_config

config = load_config()
storage = MemoryStorage()
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp: Dispatcher = Dispatcher(storage=storage)


async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запуск'),
        BotCommand(command='/help',
                   description='Справка по работе бота')]

    await bot.set_my_commands(main_menu_commands)


def authentication(func):
    """Проверка пользователя"""

    async def wrapper(message: Message):
        if message.from_user.id not in config.tg_bot.users_ids:
            return await message.reply('Доступ запрещен!', reply=False)
        return await func(message)

    return wrapper
