import json

from telebot import types


# Константи з командами
START = 'start'
HELP = 'help'
PERSONAL_DATA_MENU = 'pers_data_menu'
MAIN_MENU = 'main_menu'
SUPPORT = '/support'


# Повертає розмітку з кнопками для реплаю з відповіддю так чи ні
def get_simple_question_marcup(no_data, yes_data):
    reply_markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton('Так', callback_data=yes_data)
    no = types.InlineKeyboardButton('Ні', callback_data=no_data)
    reply_markup.row(yes, no)
    return reply_markup


# Повертає розмітку з кнопками для меню управління даними користувача
def get_personal_data_menu(user_id):
    reply_markup = types.InlineKeyboardMarkup()
    edit = types.InlineKeyboardButton('Редагувати✍️', callback_data=json.dumps({'id': user_id, 'command': '/edit_pers_data'}))
    see = types.InlineKeyboardButton('Переглянути👀', callback_data=json.dumps({'id': user_id, 'command': '/see_pers_data'}))
    delete = types.InlineKeyboardButton('Видалити🗑', callback_data=json.dumps({'id': user_id, 'command': '/rem_pers_data'}))
    reply_markup.row(edit, see)
    reply_markup.row(delete)
    return reply_markup


# Повертає розмітку з кнопками для головного меню
def get_main_menu():
    reply_markup = types.InlineKeyboardMarkup()
    choose = types.InlineKeyboardButton('Обрати рейс✈️', callback_data='/choose_flight')
    ticket_refund = types.InlineKeyboardButton('Повернути квиток↩️', callback_data='/ticket_refund')
    pers_data = types.InlineKeyboardButton('Персональні дані📁', callback_data=PERSONAL_DATA_MENU)
    support = types.InlineKeyboardButton('Підтримка📞', callback_data=SUPPORT)
    reply_markup.row(choose)
    reply_markup.row(ticket_refund)
    reply_markup.row(pers_data)
    reply_markup.row(support)
    return reply_markup
