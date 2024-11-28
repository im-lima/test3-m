from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import staff
from db import db_main

class FSMOrder(StatesGroup):
    article = State()
    size = State()
    quantity = State()
    contact_info = State()

async def start_order(message: types.Message):
    await FSMOrder.article.set()
    await message.answer('Введите артикул товара, который хотите заказать:')

async def load_article_order(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['article'] = message.text
    await FSMOrder.next()
    await message.answer('Выберите размер товара (например, S, M, L, XL):')

async def load_size_order(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await FSMOrder.next()
    await message.answer('Введите количество товара:')

async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text
    await FSMOrder.next()
    await message.answer('Введите ваш номер телефона для связи:')

async def load_contact_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact_info'] = message.text

    for staff_id in staff:
        await bot.send_message(staff_id, f"Новый заказ:\n"
                                         f"Артикул: {data['article']}\n"
                                         f"Размер: {data['size']}\n"
                                         f"Количество: {data['quantity']}\n"
                                         f"Контактные данные: {data['contact_info']}")

    await message.answer('Ваш заказ отправлен сотрудникам. Ожидайте ответа.')
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_order, commands=['order'])
    dp.register_message_handler(load_article_order, state=FSMOrder.article)
    dp.register_message_handler(load_size_order, state=FSMOrder.size)
    dp.register_message_handler(load_quantity, state=FSMOrder.quantity)
    dp.register_message_handler