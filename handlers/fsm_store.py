from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import db_main
from config import staff

cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))


class FSMStore(StatesGroup):
    product_name = State()
    category = State()
    size = State()
    price = State()
    article = State()
    photo = State()


async def start_store(message: types.Message):
    if message.from_user.id not in staff:
        await message.answer('У вас нет доступа к этой команде.')
        return

    await FSMStore.product_name.set()
    await message.answer('Введите название товара:', reply_markup=cancel)


async def load_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
    await FSMStore.next()
    await message.answer('Введите категорию товара:')


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await FSMStore.next()
    await message.answer('Выберите размер (например, S, M, L, XL):')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await FSMStore.next()
    await message.answer('Введите цену товара:')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMStore.next()
    await message.answer('Введите артикул товара:')


async def load_article(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['article'] = message.text
    await FSMStore.next()
    await message.answer('Отправьте фото товара:')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await db_main.insert_product(data['product_name'], data['category'], data['size'], data['price'], data['article'],
                                 data['photo'])
    await message.answer('Товар успешно добавлен в базу данных!')
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_store, commands=['store'])
    dp.register_message_handler(load_product_name, state=FSMStore.product_name)
    dp.register_message_handler(load_category, state=FSMStore.category)
    dp.register_message_handler(load_size, state=FSMStore.size)
    dp.register_message_handler(load_price, state=FSMStore.price)
    dp.register_message_handler(load_article, state=FSMStore.article)
    dp.register_message_handler(load_photo, state=FSMStore.photo, content_types=['photo'])