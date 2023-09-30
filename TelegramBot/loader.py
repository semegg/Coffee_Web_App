import os
import sys

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.getenv("token"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

PAYMENT_TOKEN = os.getenv('payment_token')
web_app_url = os.getenv('web_app_url')
