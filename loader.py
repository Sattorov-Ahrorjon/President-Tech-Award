from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
