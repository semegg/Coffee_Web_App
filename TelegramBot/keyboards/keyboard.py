from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from loader import web_app_url

web_app = types.WebAppInfo(url=web_app_url)

web_app_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Menu', web_app=web_app)]
    ],
    resize_keyboard=True
)


def confirm_button(user_id):
    successful_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✅ Confirm', callback_data=str(user_id))]
        ]
    )
    return successful_keyboard
