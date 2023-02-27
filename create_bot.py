from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from settings.config import load_config

config = load_config()
storage = MemoryStorage()
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher(storage=storage)


def authentication(func):
    """Проверка пользователя"""

    async def wrapper(message):
        if message['from']['id'] not in config.tg_bot.users_ids:
            return await message.reply('Доступ запрещен!', reply=False)
        return await func(message)

    return wrapper
