from config import dp, db
from aiogram import types
from captcha import Captcha
from markups import rules_mkp, menu_mkp
from functions import anti_flood


@dp.message_handler(commands='start')
@dp.throttled(anti_flood,rate=1)
async def startcmd(message: types.Message):
    
    stat = db.check_userstat(message.from_user.id)
    db.add_user(message.from_user.id, message.from_user.mention)
    if stat == 'rules':
        await message.answer(f'Правила использования бота:\n\n{db.get_rules()}', reply_markup=rules_mkp())
    elif stat == 'ban':
        await message.answer('Вы заблокированы')
    elif stat == 'ok':
        await message.answer('Вы в меню', reply_markup=menu_mkp())
    else:
        captcha = Captcha()
        captcha.register_handlers(dp)
        
        await message.answer(
            captcha.get_caption(),
            reply_markup=captcha.get_captcha_keyboard()
        )
    

@dp.message_handler(commands='id')
@dp.throttled(anti_flood,rate=1)
async def idcmd(message: types.Message):
    await message.answer(f'Ваш ID: <code>{message.from_user.id}</code>')


@dp.callback_query_handler(text='rulesok')
async def rulesokcall(call: types.CallbackQuery):
    await call.message.delete()
    db.change_status(call.from_user.id, 'ok')
    await call.message.answer('Вы в меню', reply_markup=menu_mkp())
    

@dp.callback_query_handler(text='rulesno')
async def rulesnocall(call: types.CallbackQuery):
    db.change_status(call.from_user.id, 'ban')
    await call.message.delete()
    await call.message.answer('Вы заблокированы')


@dp.callback_query_handler(text='menu')
async def menuCall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Вы в меню', reply_markup=menu_mkp())