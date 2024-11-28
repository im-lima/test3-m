from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config

staff = [1318770868, ]

token = config('TOKEN')
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)