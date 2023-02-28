from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text, Command
from create_bot import bot, authentication
from keyboards import start_kb, exit_kb
from database.orm import delete_row


@authentication
async def process_start_command(message: types.Message):
    text = f'Привет {message.from_user.first_name}!\nЯ финансовый бот для учета расходов и доходов.'
    await message.answer(text, reply_markup=start_kb)


async def cancel_handler(message: types.Message, state: FSMContext):
    """Выход из состояний"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
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
    dp.message.register(cancel_handler, Text(text='Отмена', ignore_case=True))
    dp.message.register(process_start_command, Command(commands=['start', 'help']))
    dp.message.register(continue_handler, Text(text='Продолжить'))
    dp.message.register(exit_handler, Text(text='Выход'))
    dp.message.register(delete_handler, Text(text=r'Удалить .+'))
