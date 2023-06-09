import os
from config import dp, bot, db
from aiogram import types

from markups import menu_back_mkp

@dp.callback_query_handler(text='myPurchs')
async def myPurchases (call: types.CallbackQuery):
    await call.message.delete_reply_markup()
    db.remove_old_orders()
    user_info = db.get_user_info(call.from_user.id)
    pay_count = user_info[1]
    if pay_count == None:
        pay_count = 0
    await call.message.answer(f'Ваш ID: {call.from_user.id}\nВсего покупок: {pay_count}', reply_markup=menu_back_mkp())

    waitOrderId = db.get_wait_order(call.from_user.id)
    paymentLink = db.get_payment_link(waitOrderId)

    mkp = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Проверить оплату', callback_data=paymentLink)
    mkp.add(btn)

    if waitOrderId != None:
        await bot.send_photo(call.from_user.id, open(f"{os.getcwd()}/files/cryptoQrs/{waitOrderId}.png", 'rb'))
        await bot.copy_message(call.from_user.id, call.from_user.id, int(db.get_msg_reply_id(waitOrderId)), reply_markup=mkp)