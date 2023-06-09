from config import dp, db, bot, admins, review_channel_id, review_channel_url
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import ReviewTake
from markups import cancel_mkp, menu_mkp

@dp.callback_query_handler(text_contains='reviews')
async def feedchannelmsg(call: types.CallbackQuery):
    await call.message.answer('Канал с отзывами' +': '+ review_channel_url)

@dp.callback_query_handler(text_contains='takeotziv_')
async def takeotzivcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Введите оценку от 1 до 5:', reply_markup=cancel_mkp(call.from_user.id))
    await ReviewTake.OrderId.set()
    async with state.proxy() as data:
        data['OrderId'] = call.data.split('_')[1]
    await ReviewTake.next()

@dp.message_handler(state=ReviewTake.Stars)
async def reviewtakestartmsg(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if int(message.text) > 0 and int(message.text) < 6:
            async with state.proxy() as data:
                data['Stars'] = message.text
            await message.answer('Введите ваш отзыв текстом:', reply_markup=types.InlineKeyboardMarkup(types.InlineKeyboardButton('Отменить', callback_data='cancel')))
            await ReviewTake.next()
        else:
            await message.answer('Введите оценку от 1 до 5:', reply_markup=cancel_mkp(message.from_user.id))
    else:
        await message.answer('Введите оценку числом!', reply_markup=cancel_mkp(message.from_user.id))

@dp.callback_query_handler(text='cancel', state=ReviewTake.Review)
@dp.callback_query_handler(text='cancel', state=ReviewTake.Stars)
async def reviewtakecancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в меню', reply_markup=menu_mkp())
    await state.finish()

@dp.message_handler(state=ReviewTake.Review)
async def reviewtakereviewmsg(message: types.Message, state: FSMContext):
    try:
        stars_list = ['🌟', '🌟', '🌟🌟', '🌟🌟🌟', '🌟🌟🌟🌟', '🌟🌟🌟🌟🌟']
        async with state.proxy() as data:
            pass
        order_id = data['OrderId']
        stars = data['Stars']
        goodId = db.get_order_info(int(order_id))[1]
        goodInfo = db.get_goodinfo(goodId)
        text = f'Заказ №{order_id}\nТовар: <b>{goodInfo[0]}</b>'
        if db.get_usernamerev(message.from_user.id):
            a = db.get_usernamerev(message.from_user.id)
            b = f'{a[:2]}***{a[-2:]}'
            await bot.send_message(review_channel_id, f'{text}<b>Пользователь</b>: {b}\n<b>Оценка</b>: {stars_list[int(stars)]}\n<b>Отзыв</b>: {message.text}')
        else:
            await bot.send_message(review_channel_id, f'{text}<b>Пользователь</b>: {message.from_user.first_name}\n<b>Оценка</b>: {stars_list[int(stars)]}\n<b>Отзыв</b>: {message.text}')
    except:
        for admin in admins:
            try:
                await bot.send_message(admin, 'Произошла ошибка при отправлении отзыва в канал')
            except:
                pass
    await message.answer('Спасибо. Вы были возвращены в меню', reply_markup=menu_mkp())
    await state.finish()
