from aiogram import types, Dispatcher


async def unknown_commands(message: types.Message):
    """Отлов некорректных сообщений"""
    await message.answer('Нет такой команды')


def register_other_handler(dp: Dispatcher):
    dp.message.register(unknown_commands)
