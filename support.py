from config import dp, admin_ulr
from aiogram import types

@dp.callback_query_handler(text='support')
async def suppmsg(call: types.CallbackQuery):
    await call.message.answer('Можете обратиться с вашим вопросом к этому администратору' + f" - @{admin_ulr}")