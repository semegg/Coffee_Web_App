import os

from aiogram import types
from aiogram.utils import executor

from data_base.sqlite_db import db
from keyboards.keyboard import web_app_button
from loader import dp
from payment.payment import register_payment_handlers

register_payment_handlers(dp)




@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer("Lets go", reply_markup=web_app_button)


@dp.message_handler(commands=['sales'])
async def send_sales_data(message: types.Message):
    # Викликаємо функцію для експорту даних до CSV та отримання імені файлу
    csv_filename = db.export_successful_purchases_to_csv()

    # Відправляємо файл користувачу
    with open(csv_filename, 'rb') as csv_file:
        await message.answer_document(csv_file, caption='Here is the sales data in CSV format.')

    # Видаляємо файл після відправлення
    os.remove(csv_filename)


async def on_startup(_):
    print("Coffee bot v0.1")
    db.sql_start()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
