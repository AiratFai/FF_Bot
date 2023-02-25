from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import bot, authentication
from keyboards import start_kb, exit_kb
from database.orm import delete_row


@authentication
async def start_message(message: types.Message):
    """Самый первый хендлер"""
    text = f'Привет {message.from_user.first_name}, я финансовый бот для учета расходов и доходов.'
    await bot.send_message(message.from_user.id, text, reply_markup=start_kb)


async def cancel_handler(message: types.Message, state: FSMContext):
    """Выход из состояний"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK', reply_markup=types.ReplyKeyboardRemove())


async def continue_handler(message: types.Message):
    """Возврат в стартовое меню"""
    text = 'Продолжаем работу'
    await bot.send_message(message.from_user.id, text, reply_markup=start_kb)


async def exit_handler(message: types.Message):
    """Выход"""
    text = 'Давай досвидания!'
    await bot.send_message(message.from_user.id, text, reply_markup=types.ReplyKeyboardRemove())


async def delete_handler(message: types.Message):
    """Удаление последней записи из базы данных"""
    await delete_row()
    await message.reply('Последняя строка успешно удалена', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)


# async def empty(message: types.Message):
#     """Отлов некорректных сообщений"""
#     await message.answer('Нет такой команды')
#     await message.delete()


def register_general_handlers(dp: Dispatcher):
    """Функция для регистрации хендлеров"""
    dp.register_message_handler(cancel_handler, state="*", commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(start_message, commands=['start', 'help'])
    dp.register_message_handler(continue_handler, regexp='Продолжить')
    dp.register_message_handler(exit_handler, regexp='Выход')
    dp.register_message_handler(delete_handler, regexp=r'Удалить .+')
    # dp.register_message_handler(empty)
