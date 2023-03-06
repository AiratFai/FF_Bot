from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text, Command
from create_bot import bot, authentication
from keyboards import start_kb, exit_kb
from database.orm import delete_row


@authentication
async def start_command(message: types.Message):
    text = f'Привет <b><i>{message.from_user.first_name}!</i></b>\nЯ финансовый бот. ' \
           f'Надеюсь ты заработала деньги, а не портратила)'
    await message.answer(text, reply_markup=start_kb)


async def help_command(message: types.Message):
    text = f'Данный бот предназначен для учета семейных доходов и расходов.\n' \
           f'Все записи введенные пользователями, которым разрешен доступ,\n' \
           f'сохраняются в базу данных. Также пользователи могут получить\n' \
           f'отчеты разных типов.'
    await message.answer(text)


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


@authentication
async def delete_handler(message: types.Message):
    """Удаление последней записи из базы данных"""
    await delete_row()
    await message.reply('Последняя запись успешно удалена', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, 'Продолжить работу?', reply_markup=exit_kb)


def register_general_handlers(dp: Dispatcher):
    """Функция для регистрации хендлеров"""
    dp.message.register(cancel_handler, Text(text='Отмена', ignore_case=True))
    dp.message.register(start_command, Command(commands=['start']))
    dp.message.register(help_command, Command(commands=['help']))
    dp.message.register(continue_handler, Text(text='Продолжить'))
    dp.message.register(exit_handler, Text(text='Выход'))
    dp.message.register(delete_handler, Text(text=r'Удалить последнюю запись'))
