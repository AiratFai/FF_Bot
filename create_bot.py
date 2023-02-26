from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from settings import bot_config

storage = MemoryStorage()
bot: Bot = Bot(token=bot_config.bot_token)
dp: Dispatcher(storage=storage)


def authentication(func):
    """Проверка пользователя"""

    async def wrapper(message):
        if message['from']['id'] not in [1417258138, 5140587665]:
            return await message.reply('Доступ запрещен!', reply=False)
        return await func(message)

    return wrapper
