import os
from config import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from functions import get_categories_user, get_subcategories_user, send_good
from markups import menu_mkp, promo_mkp
from payments import check_pay, createPayment, getCoins
from states import NewBuy
import qrcode


@dp.callback_query_handler(text='shop')
@dp.callback_query_handler(text='toshop')
async def toshopcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        await call.message.delete()
        await call.message.answer('Выберите категорию:', reply_markup=get_categories_user())


@dp.callback_query_handler(text_contains='usercat_')
async def usercatcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        catid = call.data.split('_')[1]
        await call.message.delete()
        await call.message.answer('Выберите подкатегорию:', reply_markup=get_subcategories_user(int(catid)))


@dp.callback_query_handler(text_contains='usersubcat_', state=NewBuy.Paying)
@dp.callback_query_handler(text_contains='usersubcat_', state=NewBuy.Promo)
@dp.callback_query_handler(text_contains='usersubcat_')
async def usersubcatcall(call: types.CallbackQuery, state: FSMContext):
    if db.check_ban(call.from_user.id):
        try:
            await state.finish()
        except:
            pass
        subcatid = call.data.split('_')[1]
        if len(db.check_goods(int(subcatid))) == 0:
            await call.answer('К сожалению тут пусто', show_alert=True)
        else:
            await call.message.delete()
            await send_good(0, int(subcatid), call.from_user.id)


@dp.callback_query_handler(text_contains='catback_')
async def catbackcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        await call.message.delete()
        subcatid = call.data.split('_')[1]
        step = call.data.split('_')[2]
        await send_good(int(step), int(subcatid), call.from_user.id)


@dp.callback_query_handler(text_contains='catnext_')
async def catnextcall(call: types.CallbackQuery):
    if db.check_ban(call.from_user.id):
        await call.message.delete()
        subcatid = call.data.split('_')[1]
        step = call.data.split('_')[2]
        await send_good(int(step), int(subcatid), call.from_user.id)


@dp.callback_query_handler(text_contains='buyGood_')
async def buyGood(call: types.CallbackQuery, state: FSMContext):
    if db.check_ban(call.from_user.id):
        await call.message.delete()
        goodId = call.data.split('_')[1]
        subCatId = call.data.split('_')[2]
        goodInfo = db.get_goodinfo(goodId)

        await NewBuy.Promo.set()
        async with state.proxy() as data:
            data['GoodId'] = {"goodId": goodId, "subCatId": subCatId}
        await call.message.answer(f'Покупка <b>{goodInfo[0]}</b>\nЦена: <b>{goodInfo[2]}</b> $\n\nВведите промокод (если есть) :', reply_markup=promo_mkp(subCatId))


@dp.message_handler(state=NewBuy.Promo)
async def newBuyPromo(message: types.Message, state: FSMContext):
    promocode = message.text
    promoInfo = db.get_promo_info(promocode)
    async with state.proxy() as data:
        goodId = data['GoodId']["goodId"]
        subCatId = data['GoodId']["subCatId"]

    if promoInfo != None:
        async with state.proxy() as data:
            data['Promo'] = promocode

        promoPercent = promoInfo[1]

        goodInfo = db.get_goodinfo(goodId)
        
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Оформить заказ', callback_data='buyOrder')
        btn2 = types.InlineKeyboardButton('Отменить покупку', callback_data=f'usersubcat_{subCatId}')
        mkp.add(btn1).add(btn2)
        
        newPrice = float(goodInfo[2]) * ((100 - int(promoPercent))/100)
        await message.answer(f'Применен промокод <b>{promocode}</b>\nЗаказ:\n\nТовар: <b>{goodInfo[0]}</b>\nЦена: <s>{goodInfo[2]}</s> <b>{newPrice}</b>\n\nХотите оформить заказ?', reply_markup=mkp)
        await NewBuy.next()

    else:
        await message.answer(f'Промокод <b>{promocode}</b> введен неверно или он не существует! Введите промокод повторно (если есть) :', reply_markup=promo_mkp(subCatId))

@dp.callback_query_handler(text='buyOrder', state=NewBuy.Paying)
@dp.callback_query_handler(text='skipPromo', state=NewBuy.Promo)
async def buyOrder(call: types.CallbackQuery, state: FSMContext):
    if db.check_ban(call.from_user.id):
        async with state.proxy() as data:
            goodId = data['GoodId']["goodId"]
            subCatId = data['GoodId']["subCatId"]
            goodInfo = db.get_goodinfo(goodId)
            if call.data == "buyOrder":
                promocode = data['Promo']
                promoInfo = db.get_promo_info(promocode)
                promoPercent = promoInfo[1]
                newPrice = float(goodInfo[2]) * ((100 - int(promoPercent))/100)
            else:
                promocode = None
                newPrice = float(goodInfo[2])

        await call.message.delete()
        orderId = db.add_order(call.from_user.id, goodId, promocode, newPrice)
        coins = await getCoins()
        mkp = types.InlineKeyboardMarkup(row_width=4)
        for coin in coins:
            mkp.insert(types.InlineKeyboardButton(coin, callback_data=f'crypto_{coin}_{orderId}_{newPrice}'))
        await call.message.answer('Выберите криптовалюту для оплаты', reply_markup=mkp)
        await state.finish()
        # await call.message.answer(f'Оформлен заказ:\nТовар: <b>{goodInfo[0]}</b>\nЦена: <b>{newPrice}</b>\n\nРеквизиты для оплаты ниже')

@dp.callback_query_handler(text_contains='crypto_')
async def cryptocall(call: types.CallbackQuery):
    await call.message.delete_reply_markup()
    crypto = call.data.split('_')[1]
    orderId = call.data.split('_')[2]
    price = call.data.split('_')[3]

    paym = await createPayment(price, crypto)
    pay_amount = paym['pay_amount']
    pay_adress = paym['pay_address']
    pay_currency = paym['pay_currency']
    pay_id = paym['payment_id']

    mkp = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Проверить оплату', callback_data=f'cryptocheck_{pay_id}_{orderId}_{price}')
    db.upd_payment_link(int(orderId), f'cryptocheck_{pay_id}_{orderId}_{price}')
    mkp.add(btn)

    img = qrcode.make(f'{pay_adress}')
    img.save(f"{os.getcwd()}/files/cryptoQrs/{orderId}.png")
    await bot.send_photo(call.from_user.id, open(f"{os.getcwd()}/files/cryptoQrs/{orderId}.png", 'rb'))
    msgId = await call.message.answer(f'Переведите: <code>{pay_amount}</code> {pay_currency}\nНа кошелек: <code>{pay_adress}</code>\n\nПосле оплаты не забудьте нажать на "Проверить оплату". Транзакция может проходить до 2-х часов', reply_markup=mkp)
    db.upd_msg_reply_id(orderId, msgId["message_id"])


@dp.callback_query_handler(text_contains='cryptocheck_')
async def cryptocheckcall(call: types.CallbackQuery):
    reply_markup = call.message.reply_markup
    await call.message.delete_reply_markup()
    pay_id = call.data.split('_')[1]
    orderId = call.data.split('_')[2]
    status = await check_pay(pay_id)
    goodId = db.get_good_for_order(orderId)


    if status == 'confirmed' or status == 'sending' or status == 'finished':
        db.pay_order(int(orderId))
        promocode = db.get_promo_from_order(orderId)
        db.use_promo(promocode)

        goodInstance = db.give_good_instance(goodId)
        instanceId = goodInstance[0]
        instanceFileName = goodInstance[1]
        instanceDescription = goodInstance[2]
        await bot.send_document(call.from_user.id, open(f'{os.getcwd()}/files/goodsInstancesFiles/{instanceFileName}', 'rb'), caption=instanceDescription)
        os.remove(f'{os.getcwd()}/files/goodsInstancesFiles/{instanceFileName}')
        os.remove(f"{os.getcwd()}/files/cryptoQrs/{orderId}.png")
        await call.message.answer('Оплата найдена, заказ оплачен. Ваш товар был отправлен выше', reply_markup=menu_mkp())

        mkp = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('Оставить отзыв', callback_data=f'takeotziv_{orderId}')
        mkp.add(btn)
        await call.message.answer('Вы можете оставить отзыв о покупке', reply_markup=mkp)

    else:
        await call.answer('Оплата не найдена, попробуйте через 5 минут', show_alert=True)
        await call.message.edit_reply_markup(reply_markup)