from aiogram import types, Dispatcher
from db import db_main

async def list_products(message: types.Message):
    products = await db_main.fetch_all_products()
    if not products:
        await message.answer('Нет товаров в базе данных.')
        return
    product_list = '\n'.join([f'ID: {product[0]} | {product[1]} | {product[2]} | {product[3]} | {product[4]} | {product[5]}'
                             for product in products])
    await message.answer(f'Список товаров:\n{product_list}')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(list_products, commands=['products'])