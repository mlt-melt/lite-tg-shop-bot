import os
from config import dp, admins, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

from markups import admin_mkp, cancel_adm_mkp, all_users_mkp, del_promo, promo_admin_mkp, promocodes, botsettings_mkp
from functions import get_faq_admin, get_categories_admin, get_good_instances_admin, get_subcategories_admin, get_goods_admin, send_admin_good
from states import AddInstance, AddPromo, NewFaq, FaqName, FaqText, AddGood, ChangePriceGood, ChangeRules, ChangeToken, AddCatRus, ChangeNamecatRus, AddSubcatRus, ChangeNamesubcatRus, ChangeNameGoodRus, ChangeDescGoodRus, RassilkaAll

@dp.message_handler(commands='admin')
async def adminCmd(message: types.Message):
    if message.from_user.id in admins:
        allOrders = db.get_orders("all")
        todayOrders = db.get_orders("today")
        weeklyOrders = db.get_orders("week")
        monthlyOrders = db.get_orders("month")

        allOrders = [[], "0"] if allOrders == [[], None] else allOrders
        todayOrders = [[], "0"] if todayOrders == [[], None] else todayOrders
        weeklyOrders = [[], "0"] if weeklyOrders == [[], None] else weeklyOrders
        monthlyOrders = [[], "0"] if monthlyOrders == [[], None] else monthlyOrders

        print(allOrders)
        print(todayOrders)
        print(weeklyOrders)
        print(monthlyOrders)

        await message.answer(f'Вы вошли в админ-панель. Статистика по боту:\n\n \
        Всего пользователей: {len(db.get_all_users())}\n \
        Товаров в боте: {len(db.get_all_goods())}\n \
        Экземпляров в боте: {len(db.get_all_instances())}\n \
        \n\
        Товаров продано всего: {len(allOrders[0])}\n \
        На сумму: {allOrders[1]}\n \
        Товаров продано за сегодня: {len(todayOrders[0])}\n \
        На сумму: {todayOrders[1]}\n \
        Товаров продано за неделю: {len(weeklyOrders[0])}\n \
        На сумму: {weeklyOrders[1]}\n \
        Товаров продано за месяц: {len(monthlyOrders[0])}\n \
        На сумму: {monthlyOrders[1]}', reply_markup=admin_mkp())
        

@dp.callback_query_handler(text='admin')
async def adminCmdCall(call: types.CallbackQuery):
    if call.from_user.id in admins:
        await call.message.delete()
        allOrders = db.get_orders("all")
        todayOrders = db.get_orders("today")
        weeklyOrders = db.get_orders("week")
        monthlyOrders = db.get_orders("month")

        allOrders = [(), "0"] if allOrders == [(None, None)] else allOrders
        todayOrders = [(), "0"] if todayOrders == [(None, None)] else todayOrders
        weeklyOrders = [(), "0"] if weeklyOrders == [(None, None)] else weeklyOrders
        monthlyOrders = [(), "0"] if monthlyOrders == [(None, None)] else monthlyOrders

        await call.message.answer(f'Вы вошли в админ-панель. Статистика по боту:\n\n \
        Всего пользователей: {len(db.get_all_users())}\n \
        Товаров в боте: {len(db.get_all_goods())}\n \
        Экземпляров в боте: {len(db.get_all_instances())}\n \
        \n\
        Товаров продано всего: {len(allOrders[0])}\n \
        На сумму: {allOrders[1]}\n \
        Товаров продано за сегодня: {len(todayOrders[0])}\n \
        На сумму: {todayOrders[1]}\n \
        Товаров продано за неделю: {len(weeklyOrders[0])}\n \
        На сумму: {weeklyOrders[1]}\n \
        Товаров продано за месяц: {len(monthlyOrders[0])}\n \
        На сумму: {monthlyOrders[1]}', reply_markup=admin_mkp())




@dp.callback_query_handler(text='promoSettings')
@dp.callback_query_handler(text='promoSettings', state=AddPromo.Promo)
async def promoSettingsCall(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    await call.message.delete()
    await call.message.answer('Промокоды:', reply_markup=promocodes())

@dp.callback_query_handler(text_contains='promo_')
async def promoCall(call: types.CallbackQuery):
    await call.message.delete()
    promoId = call.data.split('_')[1]
    await call.message.answer(f'Промокод <b>{db.get_promo_info_by_id(promoId)[0]}</b>\nХотите его удалить?', reply_markup=del_promo(promoId))

@dp.callback_query_handler(text_contains='promodel_')
async def promoDellCall(call: types.CallbackQuery):
    await call.message.delete()
    promoName = call.data.split('_')[1]
    db.del_promo(promoName=promoName)
    await call.message.answer(f'Промокод <b>{promoName}</b> удален\nВы в админ-панели', reply_markup=admin_mkp())

@dp.callback_query_handler(text='addpromo')
async def promoAddCall(call: types.CallbackQuery):
    await call.message.delete()
    await AddPromo.Promo.set()
    await call.message.answer('Введите данные о новом промокоде в таком формате (каждое новое значение на новой строке):\n\nНазвание промокода одним словом (рекомендуется вводить КАПСОМ)\nПроцент скидки целым числом\nЛимит активаций целым числом\n\nНапример:\nPROMONAME\n15\n5', reply_markup=promo_admin_mkp())

@dp.message_handler(state=AddPromo.Promo)
async def promoAdding(message: types.Message, state: FSMContext):
    try:
        promoName = message.text.split('\n')[0]
        promoPercent = message.text.split('\n')[1]
        promoActivationsLimit = message.text.split('\n')[2]
        db.add_promo(promoName, promoPercent, promoActivationsLimit)
        await message.answer(f'Промокод <b>{promoName}</b> успешно добавлен\nВы в админ-панели', reply_markup=admin_mkp())
        await state.finish()
    except:
        await message.answer("Промокод введен в неверном формате! Попробуйте зановов таком формате (каждое новое значение на новой строке):\n\nНазвание промокода одним словом (рекомендуется вводить КАПСОМ)\nПроцент скидки целым числом\nЛимит активаций целым числом\n\nНапример:\nPROMONAME\n15\n5", reply_markup=promo_admin_mkp())




@dp.callback_query_handler(text='users')
async def usersCall(call: types.CallbackQuery):
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Рассылка', callback_data='mailing')
    btn2 = types.InlineKeyboardButton('Список пользователей', callback_data='userslist')
    btn3 = types.InlineKeyboardButton('Назад', callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3)
    await call.message.answer('Выберите действие', reply_markup=mkp)

@dp.callback_query_handler(text='userslist')
async def userslistCall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Страница №1', reply_markup=all_users_mkp(1))

@dp.callback_query_handler(text_contains='userspage_')
async def userlistPageCall(call: types.CallbackQuery):
    page = call.data.split('_')[1]
    await call.message.edit_text(f'Страница №{page}', reply_markup=all_users_mkp(int(page)))

@dp.callback_query_handler(text_contains='getuser_')
async def getUserCall(call: types.CallbackQuery):
    userId = call.data.split('_')[1]
    page = call.data.split('_')[2]
    await call.message.delete()

    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Заблокировать', callback_data=f'ban_{userId}')
    btn2 = types.InlineKeyboardButton('Разблокировать', callback_data=f'banun_{userId}')
    btn3 = types.InlineKeyboardButton('Назад', callback_data=f'userspage_{page}')
    mkp.add(btn1, btn2).add(btn3)

    await call.message.answer(f'Юзер {userId} ({db.get_usernamerev(int(userId))})\n\nСтатистика:\nСтатус: {db.get_user_status(userId)}\nКуплено товаров: {db.get_user_pay_count(userId)}\nНа сумму: {db.get_user_pay_sum(userId)}', reply_markup=mkp)

@dp.callback_query_handler(text_contains='ban_')
async def banCall(call: types.CallbackQuery):
    userId = call.data.split('_')[1]
    await call.message.delete_reply_markup()
    db.ban_user(int(userId))
    await call.message.answer('Пользователь заблокирован. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    try:
        await bot.send_message(int(userId), 'Вы были заблокированы')
    except:
        pass

@dp.callback_query_handler(text_contains='banun_')
async def unbanCall(call: types.CallbackQuery):
    userId = call.data.split('_')[1]
    await call.message.delete_reply_markup()
    db.unban_user(int(userId))
    await call.message.answer('Пользователь разблокирован. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    try:
        await bot.send_message(int(userId), 'Вы были разблокированы. Пропишите /start для обновления')
    except:
        pass

@dp.callback_query_handler(text='mailing')
async def mailingCall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Введите сообщение для рассылки (можно прикрепить фото):', reply_markup=cancel_adm_mkp())
    await RassilkaAll.Text.set()

@dp.message_handler(content_types=['text', 'photo', 'video'], state=RassilkaAll.Text)
async def mailingTextMsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Text'] = message.message_id
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Отправить', callback_data='go')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    mkp.add(btn1).add(btn2)
    await message.answer(f'Вы хотите отправить данное сообщение всем пользователям?', reply_markup=mkp)

@dp.callback_query_handler(text='go', state=RassilkaAll.Text)
async def goMailingCall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer('Рассылка началась!')
    await call.message.answer('Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    async with state.proxy() as data:
        pass
    text = data['Text']
    await state.finish()
    users = db.get_all_users()
    for user in users:
        try:
            await bot.copy_message(call.from_user.id, user[1], text)
        except:
            pass
    await call.message.answer('Рассылка завершена!')

@dp.callback_query_handler(text='cancel', state=RassilkaAll.Text)
async def cancelrassilkatextcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()


@dp.callback_query_handler(text='settings')
async def cancelrassilkatextcall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Вы в настройках бота. Выберите раздел', reply_markup=botsettings_mkp())


@dp.callback_query_handler(text='changeToken')
async def changetokencall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f'Введите новый токен:', reply_markup=cancel_adm_mkp())
    await ChangeToken.Paym.set()
    await ChangeToken.next()

@dp.message_handler(state=ChangeToken.Token)
async def changetokentokenmsg(message: types.Message, state: FSMContext):
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Да', callback_data='go')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    mkp.add(btn1).add(btn2)
    async with state.proxy() as data:
        data['Token'] = message.text
    await message.answer(f'Вы действительно хотите изменить токен на <code>{message.text}</code>', reply_markup=mkp)

@dp.callback_query_handler(text='cancel', state=ChangeToken.Token)
async def changetokencancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.callback_query_handler(text='go', state=ChangeToken.Token)
async def changetokengocall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        pass
    token = data['Token']
    db.changetoken("CRYPTO", token)
    await call.message.answer('Токен успешно изменен. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.callback_query_handler(text='cancel', state=NewFaq.Name)
@dp.callback_query_handler(text='cancel', state=NewFaq.Text)
@dp.callback_query_handler(text='faqSettings')
async def faqsetcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Вы вошли панель редактирования F.A.Q.', reply_markup=get_faq_admin())
    try:
        await state.finish()
    except:
        pass

@dp.callback_query_handler(text='newfaq')
async def newfaqcall(call: types.CallbackQuery):
    await call.message.delete_reply_markup()
    await call.message.answer('Введите название раздела', reply_markup=cancel_adm_mkp())
    await NewFaq.Name.set()

@dp.message_handler(state=NewFaq.Name)
async def newfaqnamemsg(message: types.Message, state: FSMContext):
    await message.answer(f'Хорошо, название будет: <code>{message.text}</code>')
    async with state.proxy() as data:
        data['Name'] = message.text
    await message.answer('Введите текст к разделу:', reply_markup=cancel_adm_mkp())
    await NewFaq.next()

@dp.message_handler(state=NewFaq.Text)
async def newfaqtextmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Text'] = message.text
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Пропустить', callback_data='skip')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    mkp.add(btn1).add(btn2)
    await message.answer('Отправьте фото или нажмите "Пропустить"', reply_markup=mkp)
    await NewFaq.next()

@dp.callback_query_handler(text='skip', state=NewFaq.Photo)
async def skipnewfawphotocall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        pass
    db.add_faq(data['Name'], data['Text'], 'None')
    await call.message.answer('Успешно добавлено! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(content_types='photo', state=NewFaq.Photo)
async def newfaqphotoctphoto(message: types.message, state: FSMContext):
    file_info = await bot.get_file(message.photo[-1].file_id)
    filename = file_info.file_path.split('/')[-1]
    await bot.download_file(file_info.file_path, f'{os.getcwd()}/images/{filename}')
    async with state.proxy() as data:
        data['Photo'] = filename
    db.add_faq(data['Name'], data['Text'], filename)
    await message.answer('Успешно добавлено! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()



@dp.callback_query_handler(text_contains='changefaq_')
async def changefaqcall(call: types.CallbackQuery):
    faq_info = db.get_faq(int(call.data.split('_')[1]))
    faqid = call.data.split('_')[1]
    await call.message.delete_reply_markup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Название', callback_data=f'changefaqname_{faqid}')
    btn2 = types.InlineKeyboardButton('Текст', callback_data=f'changefaqtext_{faqid}')
    btn3 = types.InlineKeyboardButton('Удалить', callback_data=f'delfaq_{faqid}')
    btn4 = types.InlineKeyboardButton('Отменить', callback_data='faqset')
    mkp.add(btn1, btn2).add(btn3).add(btn4)
    if faq_info[2] == 'None' or faq_info[2] == None:
        await call.message.answer(f'Выбран раздел: <code>{faq_info[0]}</code>\n\n{faq_info[1]}', reply_markup=mkp)
    else:
        await call.message.answer_photo(open(f'{os.getcwd()}/images/{faq_info[2]}', 'rb'), caption=f'Выбран раздел: <code>{faq_info[0]}</code>\n\n{faq_info[1]}', reply_markup=mkp)


@dp.callback_query_handler(text_contains='changefaqname_')
async def changefaqnamecall(call: types.CallbackQuery, state: FSMContext):
    faqid = call.data.split('_')[1]
    faq_info = db.get_faq(int(faqid))
    await call.message.delete()
    await call.message.answer(f'Старое название раздела: <code>{faq_info[0]}</code>\nВведите новое:', reply_markup=cancel_adm_mkp())
    await FaqName.FaqId.set()
    async with state.proxy() as data:
        data['FaqId'] = faqid


@dp.callback_query_handler(text='cancel', state=FaqName.FaqId)
@dp.callback_query_handler(text='cancel', state=FaqName.Name)
@dp.callback_query_handler(text='cancel', state=FaqText.FaqId)
@dp.callback_query_handler(text='cancel', state=FaqText.Text)
async def faqnamefaqidcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(state=FaqName.FaqId)
async def faqnamefaqidmsg(message: types.Message, state: FSMContext):
    await FaqName.next()
    async with state.proxy() as data:
        data['Name'] = message.text
    faqid = data['FaqId']
    db.changefaq_name(int(faqid), message.text)
    await message.answer('Название успешно изменено. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()



@dp.callback_query_handler(text_contains='changefaqtext_')
async def changefaqtextcall(call: types.CallbackQuery, state: FSMContext):
    faqid = call.data.split('_')[1]
    faq_info = db.get_faq(int(faqid))
    await call.message.delete()
    await call.message.answer(f'Старый текст раздела: <code>{faq_info[1]}</code>\nВведите новый:', reply_markup=cancel_adm_mkp())
    await FaqText.FaqId.set()
    async with state.proxy() as data:
        data['FaqId'] = faqid


@dp.message_handler(state=FaqText.FaqId)
async def faqtextfaqidmsg(message: types.Message, state: FSMContext):
    await FaqText.next()
    async with state.proxy() as data:
        data['Text'] = message.text
    faqid = data['FaqId']
    db.changefaq_text(int(faqid), message.text)
    await message.answer('Текст раздела успешно изменен. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()


@dp.callback_query_handler(text_contains='delfaq_')
async def delfaqcall(call: types.CallbackQuery):
    faqid = call.data.split('_')[1]
    faq_info = db.get_faq(int(faqid))
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Удалить', callback_data=f'delfaqq_{faqid}')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='faqset')
    mkp.add(btn1).add(btn2)
    await call.message.answer(f'Вы действительно хотите удалить раздел <code>{faq_info[0]}</code>', reply_markup=mkp)

@dp.callback_query_handler(text_contains='delfaqq_')
async def delfaqqcall(call: types.CallbackQuery):
    faqid = call.data.split('_')[1]
    await call.message.delete_reply_markup()
    db.del_faq(int(faqid))
    await call.message.answer('Раздел успешно удален. Вы были возвращены в админ-панель', reply_markup=admin_mkp())



@dp.callback_query_handler(text='changeRules')
async def changerulesmsg(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(f'Текущие правила:\n\n{db.get_rules()}')
    await call.message.answer('Введите новый правила:', reply_markup=cancel_adm_mkp())
    await ChangeRules.Rules.set()


@dp.callback_query_handler(text='cancel', state=ChangeRules.Rules)
async def cancelchangerulescall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(state=ChangeRules.Rules)
async def changerulesrulesmsg(message: types.Message, state: FSMContext):
    db.changerules(message.text)
    await message.answer('Правила успешно обновлены! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()






@dp.callback_query_handler(text='cancel', state=AddCatRus.CatName)
@dp.callback_query_handler(text='cancel', state=AddSubcatRus.SubcatName)
@dp.callback_query_handler(text='cancel', state=AddSubcatRus.SubcatName)
async def orderscall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Выберите категорию/действие:', reply_markup=get_categories_admin())
    try:
        await state.finish()
    except:
        pass

@dp.callback_query_handler(text='shopSettings')
async def productscall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Выберите категорию/действие:', reply_markup=get_categories_admin())

@dp.callback_query_handler(text='addcat')
async def addcatcall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Введите название категории:', reply_markup=cancel_adm_mkp())
    await AddCatRus.CatName.set()

@dp.message_handler(state=AddCatRus.CatName)
async def addcatruscatnamemsg(message: types.Message, state: FSMContext):
    db.add_cat(message.text)
    await message.answer('Категория успешно добавлена! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()


@dp.callback_query_handler(text_contains='admincat_', state=ChangeNamecatRus.CatId)
@dp.callback_query_handler(text_contains='admincat_', state=ChangeNamecatRus.CatName)
@dp.callback_query_handler(text_contains='admincat_')
async def admincatcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    cat_id = call.data.split('_')[1]
    cat_name = db.get_cat_name(int(cat_id))
    await call.message.answer(f'Категория: <code>{cat_name}</code>\nВыберите, подкатегорию/действие:', reply_markup=get_subcategories_admin(int(cat_id)))
    try:
        await state.finish()
    except:
        pass


@dp.callback_query_handler(text_contains='addsubcat_')
async def addsubcatcall(call: types.CallbackQuery, state: FSMContext):
    cat_id = call.data.split('_')[1]
    await call.message.delete()
    await call.message.answer('Введите название подкатегории', reply_markup=cancel_adm_mkp())
    await AddSubcatRus.CatId.set()
    async with state.proxy() as data:
        data['CatId'] = cat_id
    await AddSubcatRus.next()

@dp.message_handler(state=AddSubcatRus.SubcatName)
async def addsubcatrussubcatnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    catid = data['CatId']
    db.add_subcat(int(catid), message.text)
    await message.answer('Подкатегория успешно добавлена! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()



@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.Name)
@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.Description)
@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.Photo)
@dp.callback_query_handler(text_contains='adminsubcat_', state=AddGood.Price)
@dp.callback_query_handler(text_contains='adminsubcat_', state=ChangeNamesubcatRus.SubcatId)
@dp.callback_query_handler(text_contains='adminsubcat_', state=ChangeNamesubcatRus.SubcatName)
@dp.callback_query_handler(text_contains='adminsubcat_')
async def adminsubcatcall(call: types.CallbackQuery, state: FSMContext):
    subcat_id = call.data.split('_')[1]
    cat_id = call.data.split('_')[2]
    subcat_name = db.get_subcat_name(int(subcat_id))
    await call.message.delete()
    await call.message.answer(f'Подкатегория: <code>{subcat_name}</code>\nВыберите товар/действие:', reply_markup=get_goods_admin(int(subcat_id), cat_id))
    try:
        await state.finish()
    except:
        pass

@dp.callback_query_handler(text_contains='changenamecat_')
async def changenamecatcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    cat_id = call.data.split('_')[1]
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вернуться', callback_data=f'admincat_{cat_id}')
    mkp.add(btn1)
    await call.message.answer('Введите новое название категории:', reply_markup=mkp)
    await ChangeNamecatRus.CatId.set()
    async with state.proxy() as data:
        data['CatId'] = cat_id

@dp.message_handler(state=ChangeNamecatRus.CatId)
async def changenamecatruscatidmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    cat_id = data['CatId']
    db.changename_cat(int(cat_id), message.text)
    await message.answer('Название категории успешно изменено! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()


@dp.callback_query_handler(text_contains='changenamesubcat_')
async def changenamesubcatcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    subcat_id = call.data.split('_')[1]
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вернуться', callback_data=f'adminsubcat_{subcat_id}')
    mkp.add(btn1)
    await call.message.answer('Введите новое название подкатегории:', reply_markup=mkp)
    await ChangeNamesubcatRus.SubcatId.set()
    async with state.proxy() as data:
        data['SubcatId'] = subcat_id

@dp.message_handler(state=ChangeNamesubcatRus.SubcatId)
async def changenamesubcatrusmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    subcatid = data['SubcatId']
    db.changename_subcat(int(subcatid), message.text)
    await message.answer('Название подкатегории успешно изменено! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()


@dp.callback_query_handler(text_contains='addgood_')
async def addgoodcall(call: types.CallbackQuery, state: FSMContext):
    subcatid = call.data.split('_')[1]
    cat_id = call.data.split('_')[2]
    await AddGood.SubcatId.set()
    await AddGood.CatId.set()
    async with state.proxy() as data:
        data['SubcatId'] = subcatid
        data['CatId'] = cat_id
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Отменить', callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1)
    await call.message.answer('Введите название товара:', reply_markup=mkp)
    await AddGood.next()


@dp.message_handler(state=AddGood.Name)
async def addgoodnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Name'] = message.text
    subcatid = data['SubcatId']
    cat_id = data['CatId'] 
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Отменить', callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1)
    await message.answer('Введите описание к товару:', reply_markup=mkp)
    await AddGood.next()

@dp.message_handler(state=AddGood.Description)
async def addgooddescriptionmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Description'] = message.text
    subcatid = data['SubcatId']
    cat_id = data['CatId']
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Пропустить', callback_data='skip')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1).add(btn2)
    await message.answer('Отправьте фото или нажмите пропустить', reply_markup=mkp)
    await AddGood.next()

@dp.message_handler(content_types='photo', state=AddGood.Photo)
async def addgoodphotophoto(message: types.Message, state: FSMContext):
    file_info = await bot.get_file(message.photo[-1].file_id)
    filename = file_info.file_path.split('/')[-1]
    await bot.download_file(file_info.file_path, f'{os.getcwd()}/images/{filename}')
    async with state.proxy() as data:
        data['Photo'] = filename
    subcatid = data['SubcatId']
    cat_id = data['CatId'] 
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Отменить', callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1)
    await message.answer('Введите цену (целым числом, либо через точку, например: <code>249.50</code>)', reply_markup=mkp)
    await AddGood.next()

@dp.callback_query_handler(text='skip', state=AddGood.Photo)
async def addgoodphotoskipcall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['Photo'] = 'None'
    subcatid = data['SubcatId']
    cat_id = data['CatId'] 
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Отменить', callback_data=f'adminsubcat_{subcatid}_{cat_id}')
    mkp.add(btn1)
    await call.message.delete_reply_markup()
    await call.message.answer('Введите цену (целым числом, либо через точку, например: <code>249.50</code>)', reply_markup=mkp)
    await AddGood.next()


@dp.message_handler(state=AddGood.Price)
async def addgoodprice(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        async with state.proxy() as data:
            data['Price'] = price
        subcatid = data['SubcatId']
        cat_id = data['CatId'] 
        name = data['Name']
        description = data['Description']
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Добавить', callback_data='add')
        btn2 = types.InlineKeyboardButton('Отменить', callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1).add(btn2)
        
        if data['Photo'] == 'None':
            await message.answer(f'Название товара: <code>{name}</code>\nОписание: <code>{description}</code>\nЦена: <code>{price}</code>', reply_markup=mkp)
        else:
            photo = data['Photo']
            await message.answer_photo(open(f'{os.getcwd()}/images/{photo}', 'rb'), caption=f'Название товара: <code>{name}</code>\nОписание: <code>{description}</code>\nЦена: <code>{price}</code>', reply_markup=mkp)

    except Exception as ex:
        print(ex)
        async with state.proxy() as data:
            pass
        subcatid = data['SubcatId']
        cat_id = data['CatId'] 
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Отменить', callback_data=f'adminsubcat_{subcatid}_{cat_id}')
        mkp.add(btn1)
        await message.answer('Вы неправильно ввели цену! Введите цену целым числом, либо через точку, например: <code>249.50</code>')

@dp.callback_query_handler(text='add', state=AddGood.Price)
async def addgoodpricecalladd(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    subcat_id = data['SubcatId']
    name = data['Name']
    description = data['Description']
    photo = data['Photo']
    price = data['Price']
    db.add_good(subcat_id, name, description, photo, price)
    await call.message.delete()
    await call.message.answer('Товар был успешно добавлен! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()


@dp.callback_query_handler(text_contains='admingood_', state=ChangePriceGood.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeDescGoodRus.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeDescGoodRus.GoodDesc)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeNameGoodRus.GoodId)
@dp.callback_query_handler(text_contains='admingood_', state=ChangeNameGoodRus.GoodName)
@dp.callback_query_handler(text_contains='admingood_')
async def admingoodcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn6 = types.InlineKeyboardButton('Экземпляры товара', callback_data=f'instances_{goodid}')
    btn1 = types.InlineKeyboardButton('Название', callback_data=f'changegoodname_{goodid}')
    btn2 = types.InlineKeyboardButton('Описание', callback_data=f'changegooddesc_{goodid}')
    btn3 = types.InlineKeyboardButton('Цену', callback_data=f'changegoodprice_{goodid}')
    btn4 = types.InlineKeyboardButton('Удалить', callback_data=f'delgood_{goodid}')
    btn5 = types.InlineKeyboardButton('Отменить', callback_data='admin')
    mkp.add(btn6).add(btn1).add(btn2, btn3).add(btn4).add(btn5)
    if good_info[3] == 'None':
        await call.message.answer(f'Название товара: <code>{good_info[0]}</code>\nОписание товара: <code>{good_info[1]}</code>\nЦена: <code>{good_info[2]} $</code>\n\nВыберите, что вы хотите изменить', reply_markup=mkp)
    else:
        await call.message.answer_photo(open(f'{os.getcwd()}/images/{good_info[3]}', 'rb'), caption=f'Название товара: <code>{good_info[0]}</code>\nОписание товара: <code>{good_info[1]}</code>\nЦена: <code>{good_info[2]} $</code>\n\nВыберите, что вы хотите изменить', reply_markup=mkp)
    try:
        await state.finish()
    except:
        pass


@dp.callback_query_handler(text_contains='changegoodname_')
async def changegoodnamecall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вернуться', callback_data=f'admingood_{goodid}')
    mkp.add(btn1)
    await call.message.answer(f'Введите новое название для товара <code>{good_info[0]}</code>', reply_markup=mkp)
    await ChangeNameGoodRus.GoodId.set()
    async with state.proxy() as data:
        data['GoodId'] = goodid

@dp.message_handler(state=ChangeNameGoodRus.GoodId)
async def changenamegoodrusmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    db.change_namegood(int(goodid), message.text)
    await send_admin_good(int(goodid), message.from_user.id)
    await state.finish()

@dp.callback_query_handler(text_contains='changegooddesc_')
async def changegooddesccall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вернуться', callback_data=f'admingood_{goodid}')
    mkp.add(btn1)
    await call.message.answer(f'Введите новое описание для товара <code>{good_info[0]}</code>', reply_markup=mkp)
    await ChangeDescGoodRus.GoodId.set()
    async with state.proxy() as data:
        data['GoodId'] = goodid

@dp.message_handler(state=ChangeDescGoodRus.GoodId)
async def changedescgoodrusmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    db.change_descgood(int(goodid), message.text)
    await send_admin_good(int(goodid), message.from_user.id)
    await state.finish()



@dp.callback_query_handler(text_contains='changegoodprice_')
async def changegoodpricecall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вернуться', callback_data=f'admingood_{goodid}')
    mkp.add(btn1)
    await call.message.answer(f'Введите новую цену для товара <code>{good_info[0]}</code>', reply_markup=mkp)
    await ChangePriceGood.GoodId.set()
    async with state.proxy() as data:
        data['GoodId'] = goodid

@dp.message_handler(state=ChangePriceGood.GoodId)
async def changepricegoodgoodidmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    goodid = data['GoodId']
    try:
        price = float(message.text)

        db.change_pricegood(int(goodid), price)

        await send_admin_good(int(goodid), message.from_user.id)
        await state.finish()
    except:
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Вернуться', callback_data=f'admingood_{goodid}')
        mkp.add(btn1)
        await message.answer('Введите цену целым числом, либо через точку, например <code>149.50</code>', reply_markup=mkp)

@dp.callback_query_handler(text_contains='delgood_')
async def delgoodcall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodid))
    await call.message.delete_reply_markup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Удалить', callback_data=f'delgoodd_{goodid}')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data=f'admingood_{goodid}')
    mkp.add(btn1, btn2)
    await call.message.answer(f'Вы действительно хотите удалить товар <code>{good_info[0]}</code>?', reply_markup=mkp)


@dp.callback_query_handler(text_contains='delgoodd_')
async def delgooddcall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    db.del_good(int(goodid))
    await call.message.delete()
    await call.message.answer('Товар успешно удален! Вы были возвращены в админ-панель', reply_markup=admin_mkp())

@dp.callback_query_handler(text_contains='delcat_')
async def delcatcall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    catname = db.get_namecat(int(catid))
    await call.message.delete_reply_markup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Удалить', callback_data=f'delcatt_{catid}')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='admin')
    mkp.add(btn1, btn2)
    await call.message.answer(f'Вы действительно хотите удалить категорию <code>{catname}</code>?', reply_markup=mkp)


@dp.callback_query_handler(text_contains='delcatt_')
async def delcattcall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    db.del_cat(int(catid))
    await call.message.delete()
    await call.message.answer('Категория успешно удалена! Вы были возвращены в админ-панель', reply_markup=admin_mkp())


@dp.callback_query_handler(text_contains='delsubcat_')
async def delSubcatCall(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    subcatname = db.get_namesubcat(int(subcatid))
    await call.message.delete_reply_markup()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Удалить', callback_data=f'delsubcatt_{subcatid}')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='admin')
    mkp.add(btn1, btn2)
    await call.message.answer(f'Вы действительно хотите удалить категорию <code>{subcatname}</code>?', reply_markup=mkp)

@dp.callback_query_handler(text_contains='delsubcatt_')
async def delSubcatCallGo(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    await call.message.delete()
    db.del_subcat(int(subcatid))
    await call.message.answer('Подкатегория успешно удалена! Вы были возвращены в админ-панель', reply_markup=admin_mkp())



@dp.callback_query_handler(text_contains='instances_')
@dp.callback_query_handler(text_contains='instances_', state=AddInstance.GoodId)
async def goodInstancesCall(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.finish()
    except:
        pass
    goodId = call.data.split('_')[1]
    good_info = db.get_goodinfo(int(goodId))
    await call.message.delete()
    goods_list = db.get_good_instances(goodId)
    await call.message.answer(f'Товар <b>{good_info[0]}</b>\nОписание: <b>{good_info[1]}</b>\nЦена: <b>{good_info[2]}</b>$\n\nГотово экземпляров к продаже: {len(goods_list)} шт.\nВыберите действие', reply_markup=get_good_instances_admin(goodId))

@dp.callback_query_handler(text_contains='addinstance_')
async def addInstancesCall(call: types.CallbackQuery, state: FSMContext):
    goodId = call.data.split('_')[1]
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Отменить', callback_data=f'instances_{goodId}')
    mkp.add(btn)
    await call.message.answer('Отправьте файл/фото/видео для экземпляра\n(Из-за ограничений телеграма боты не могут оперировать файлами более 20 Мб. Если вес файла превышает эту цифру следует воспользоваться файлообменником и оставить ссылку на товар в описании)', reply_markup=mkp)
    await AddInstance.GoodId.set()
    async with state.proxy() as data:
        data['GoodId'] = goodId

@dp.message_handler(content_types=['document', 'photo', 'video'], state=AddInstance.GoodId)
async def addInstancesFileCall(message: types.Message, state: FSMContext):
    if message.document:
        file_info = await bot.get_file(message.document.file_id)
    elif message.photo:
        file_info = await bot.get_file(message.photo[-1].file_id)
    elif message.video:
        file_info = await bot.get_file(message.video[-1].file_id)
    filename = file_info.file_path.split('/')[-1]
    await bot.download_file(file_info.file_path, f'{os.getcwd()}/files/goodsInstancesFiles/{filename}')
    async with state.proxy() as data:
        goodId = data['GoodId']
        data['FileName'] = filename
    mkp = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton('Отменить', callback_data=f'instances_{goodId}')
    mkp.add(btn)
    await message.answer("Хорошо, теперь отправьте описание", reply_markup=mkp)
    await AddInstance.next()

@dp.message_handler(state=AddInstance.FileName)
async def addInstancesDescriptionCall(message: types.Message, state: FSMContext):
    description = message.text
    async with state.proxy() as data:
        goodId = data['GoodId']
        filename = data['FileName']
    db.add_good_instance(goodId, filename, description)
    good_info = db.get_goodinfo(int(goodId))
    goods_list = db.get_good_instances(goodId)
    await message.answer(f"Экземпляров добавлен в товар. Вы в меню товара <b>{good_info[0]}</b>\nОписание: <b>{good_info[1]}</b>\nЦена: <b>{good_info[2]}</b>$\n\nГотово к продаже: {len(goods_list)} экземпляров\nВыберите действие", reply_markup=get_good_instances_admin(goodId))
    await state.finish()


@dp.callback_query_handler(text_contains='Allinstancesdel_')
async def delSubcatCallGo(call: types.CallbackQuery):
    goodId = call.data.split('_')[1]
    await call.message.delete()
    good_info = db.get_goodinfo(int(goodId))
    goods_list = db.get_good_instances(goodId)
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Удалить', callback_data=f'delinstancesGO_{goodId}')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data=f'instances_{goodId}')
    mkp.add(btn1, btn2)
    await call.message.answer(f'Вы действительно хотите удалить {len(goods_list)} шт. экземпляров для товара {good_info[0]}?', reply_markup=mkp)


@dp.callback_query_handler(text_contains='delinstancesGO_')
async def delSubcatCallGo(call: types.CallbackQuery):
    goodId = call.data.split('_')[1]
    await call.message.delete()
    good_info = db.get_goodinfo(int(goodId))
    db.del_all_instances(goodId)
    await call.message.answer(f'Все экземпляры для товара {good_info[0]} удалены, вы возвращены в админ-панель', reply_markup=admin_mkp())