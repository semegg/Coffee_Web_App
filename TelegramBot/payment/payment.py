import datetime

from aiogram import types
from aiogram.types.message import ContentType
from data_base.sqlite_db import db
from keyboards.keyboard import confirm_button
from loader import bot, PAYMENT_TOKEN


async def cmd_buy(web_app_message):
    web_data = web_app_message.web_app_data.data
    price, payload = db.set_prices_for_payment(web_data)
    await bot.send_message(web_app_message.chat.id,
                           " Real cards won't work with me, no money will be debited from your account."
                           " Use this test card number to pay for your Coffee order: `4444 3333 2222 1111`"
                           "\n\nThis is your demo invoice:", parse_mode='Markdown')
    await bot.send_invoice(web_app_message.chat.id,
                           title='Order',
                           description='discription',
                           provider_token=PAYMENT_TOKEN,
                           currency='uah',
                           prices=price,
                           start_parameter='example',
                           payload=payload)


async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Hoooooray! Thanks for payment! We will proceed your order for `{} {}`'
                           ' as fast as possible! Stay in touch.'
                           '\n'.format(
                               message.successful_payment.total_amount / 100, message.successful_payment.currency),
                           parse_mode='Markdown')

    await bot.send_message(chat_id=439325490,
                           text='Замовник : <a href="{}">{}</a>\n'
                                '--------------------------\n'
                                'Замовлення:\n{}\nСумма замовлення: <b>{}₴</b>'
                           .format(message.from_user.url,
                                   message.from_user.full_name,
                                   message.successful_payment.invoice_payload,
                                   message.successful_payment.total_amount / 100
                                   , ), reply_markup=confirm_button(message.from_user.id))
    db.succesful_sales(
        user_profile_url=message.from_user.url,
        user_name=message.from_user.full_name,
        order=message.successful_payment.invoice_payload,
        total_amount=message.successful_payment.total_amount / 100,
        date=datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    )


async def coffee_is_ready(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.data,
                           text="Thank you for your 'payment'! Don't worry, your imaginary credit card was not charged. Your order is not on the way.")


def register_payment_handlers(dp):
    dp.register_message_handler(cmd_buy, content_types=['web_app_data'])
    dp.register_pre_checkout_query_handler(checkout, lambda query: True)
    dp.register_message_handler(got_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_callback_query_handler(coffee_is_ready)
