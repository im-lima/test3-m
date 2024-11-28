import logging
from aiogram import executor
from config import bot, dp, staff
from db import db_main
from handlers import commands, fsm_store, fsm_orders, products

async def on_startup(_):
    for admin in staff:
        await bot.send_message(chat_id=admin, text='Бот включен!')
    await db_main.create_tables()

async def on_shutdown(_):
    for admin in staff:
        await bot.send_message(chat_id=admin, text='Бот выключен!')

commands.register_commands(dp)
fsm_store.register_handlers(dp)
fsm_orders.register_handlers(dp)
products.register_handlers(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)