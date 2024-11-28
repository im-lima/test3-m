from aiogram import types, Dispatcher
from config import bot, staff

async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}!\n'
                         f'Твой Telegram Id - {message.from_user.id}')

async def info(message: types.Message):
    await message.answer('Этот бот помогает сотрудникам добавлять товары в базу и обрабатывать заказы. '
                         'Клиенты могут заказывать товары, и вы будете получать уведомления.')

def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(info, commands=["info"])