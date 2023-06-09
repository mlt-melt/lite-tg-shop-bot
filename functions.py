import os
from config import db, bot
from aiogram import types

def get_faq_admin():
    faq_list = db.get_all_faq_adm()
    mkp = types.InlineKeyboardMarkup()
    for i in faq_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'changefaq_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('Новый раздел', callback_data='newfaq'))
    mkp.add(types.InlineKeyboardButton('Вернуться в админ-панель', callback_data='admin'))
    return mkp


def get_faq_user():
    faq_list = db.get_all_faq()
    mkp = types.InlineKeyboardMarkup()
    for i in faq_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'getfaq_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('Вернуться в меню', callback_data='tomenu'))
    return mkp


def get_categories_admin():
    cat_list = db.get_all_cat_adm()
    mkp = types.InlineKeyboardMarkup()
    for i in cat_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'admincat_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('➕ Добавить категорию', callback_data='addcat'))
    mkp.add(types.InlineKeyboardButton('🔙 Вернуться в админ-панель', callback_data='admin'))
    return mkp

def get_categories_user():
    cat_list = db.get_all_cat()
    mkp = types.InlineKeyboardMarkup()
    for i in cat_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'usercat_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('Вернуться в меню', callback_data='tomenu'))
    return mkp

def get_subcategories_admin(cat_id):
    subcat_list = db.get_subcat_adm(cat_id)
    mkp = types.InlineKeyboardMarkup()
    for i in subcat_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'adminsubcat_{i[0]}_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('➕ Добавить подкатегорию', callback_data=f'addsubcat_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('📝 Изменить название', callback_data=f'changenamecat_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('🗑 Удалить категорию', callback_data=f'delcat_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('🔙 Вернуться', callback_data='shopSettings'))
    return mkp

def get_subcategories_user(cat_id):
    subcat_list = db.get_subcat(cat_id)
    mkp = types.InlineKeyboardMarkup()
    for i in subcat_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'usersubcat_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('🔙 Вернуться', callback_data='toshop'))
    return mkp


def get_goods_admin(subcat_id, cat_id):
    goods_list = db.get_goods(subcat_id)
    mkp = types.InlineKeyboardMarkup()
    for i in goods_list:
        mkp.add(types.InlineKeyboardButton(i[1], callback_data=f'admingood_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('➕ Добавить товар', callback_data=f'addgood_{subcat_id}_{cat_id}'))
    mkp.add(types.InlineKeyboardButton('📝 Изменить название', callback_data=f'changenamesubcat_{subcat_id}'))
    mkp.add(types.InlineKeyboardButton('🗑 Удалить подкатегорию', callback_data=f'delsubcat_{subcat_id}'))
    mkp.add(types.InlineKeyboardButton('🔙 Вернуться', callback_data=f'admincat_{cat_id}'))
    return mkp

def get_good_instances_admin(goodId):
    mkp = types.InlineKeyboardMarkup()
    mkp.add(types.InlineKeyboardButton('➕ Добавить экземпляр', callback_data=f'addinstance_{goodId}'))
    mkp.add(types.InlineKeyboardButton('🗑 Удалить все экземпляры', callback_data=f'Allinstancesdel_{goodId}'))
    mkp.add(types.InlineKeyboardButton('🔙 Вернуться', callback_data=f'admingood_{goodId}'))
    return mkp

async def send_admin_good(goodid, user_id):
    good_info = db.get_goodinfo(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    mkp = types.InlineKeyboardMarkup()
    btn6 = types.InlineKeyboardButton('Экземпляры товара', callback_data=f'instances_{goodid}')
    btn1 = types.InlineKeyboardButton('Название', callback_data=f'changegoodname_{goodid}')
    btn2 = types.InlineKeyboardButton('Описание', callback_data=f'changegooddesc_{goodid}')
    btn3 = types.InlineKeyboardButton('Цену', callback_data=f'changegoodprice_{goodid}')
    btn4 = types.InlineKeyboardButton('Удалить', callback_data=f'delgood_{goodid}')
    btn5 = types.InlineKeyboardButton('Отменить', callback_data='admin')
    mkp.add(btn6).add(btn1).add(btn2, btn3).add(btn4).add(btn5)
    if good_info[3] == 'None':
        await bot.send_message(user_id, f'Название товара: <code>{good_info[0]}</code>\nОписание товара: <code>{good_info[1]}</code>\nЦена: <code>{good_info[2]}</code>\n\nВыберите, что вы хотите изменить', reply_markup=mkp)
    else:
        await bot.send_photo(user_id, open(f'{os.getcwd()}/images/{good_info[3]}', 'rb'), caption=f'Название товара: <code>{good_info[0]}</code>\nОписание товара: <code>{good_info[1]}</code>\nЦена: <code>{good_info[2]}</code>\n\nВыберите, что вы хотите изменить', reply_markup=mkp)


async def send_good(step, subcatid, user_id):
    goods = db.get_goods_user(subcatid)

    name = goods[step][1]
    description = goods[step][2]
    price = goods[step][3]
    price = float(price)
    price = f'{price:.2f}'
    photo = goods[step][4]
    goodid = goods[step][0]

    nowCat = db.get_cat_id_by_subcat_id(subcatid)
    mkp = types.InlineKeyboardMarkup()
    if step == 0:
        btn1 = types.InlineKeyboardButton('❌', callback_data='none')
    else:
        btn1 = types.InlineKeyboardButton('⬅', callback_data=f'catback_{subcatid}_{step-1}')
    btn2 = types.InlineKeyboardButton(f'{step+1}/{len(goods)}', callback_data='none')
    if step+1 == len(goods):
        btn3 = types.InlineKeyboardButton('❌', callback_data='none')
    else:
        btn3 = types.InlineKeyboardButton('➡', callback_data=f'catnext_{subcatid}_{step+1}')
    btn7 = types.InlineKeyboardButton('Купить', callback_data=f'buyGood_{goodid}_{subcatid}')
    btn8 = types.InlineKeyboardButton('Назад', callback_data=f'usercat_{nowCat}')
    print(db.get_good_instances(goodid))
    if db.get_good_instances(goodid) != []:
        mkp.add(btn1, btn2, btn3).add(btn7).add(btn8)
        allSold = ''
    else:
        mkp.add(btn1, btn2, btn3).add(btn8)
        allSold = '\n\nНА ДАННЫЙ МОМЕНТ ТОВАРА НЕТ В НАЛИЧИИ ❗️'

    if photo == 'None':
        await bot.send_message(user_id, f'<b>Название товара</b>: <code>{name}</code>\n<b>Описание</b>: {description}\n<b>Цена</b>: <code>{price}</code> ${allSold}', reply_markup=mkp)
    else:
        await bot.send_photo(user_id, open(f'{os.getcwd()}/images/{photo}', 'rb'), caption=f'<b>Название товара</b>: <code>{name}</code>\n<b>Описание</b>: {description}\n<b>Цена</b>: <code>{price}</code> ${allSold}', reply_markup=mkp)


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer("Не флуди")