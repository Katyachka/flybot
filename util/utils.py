import json

from telebot import types


# Константи з командами
START = 'start'
HELP = 'help'
PERSONAL_DATA_MENU = 'pers_data_menu'
MAIN_MENU = 'main_menu'
CHOOSE_FLIGHT = 'choose_flight'
TICKETS = 'tickets'
SUPPORT = 'support'
CREATE_PERS_DATA = 'create_pers_data'
EDIT_PERS_DATA = 'edit_pers_data'
SEE_PERS_DATA = 'see_pers_data'
REM_PERS_DATA = 'rem_pers_data'
EDIT_GENDER = 'edit_gender'


# Повертає розмітку з кнопками для реплаю з відповіддю так чи ні
def get_simple_question_marcup(yes_data, no_data):
    reply_markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton('Так', callback_data=yes_data)
    no = types.InlineKeyboardButton('Ні', callback_data=no_data)
    reply_markup.row(yes, no)
    return reply_markup


# Повертає розмітку з кнопками для реплаю з 2 варінтами відповіді
def get_simple_question_marcup_with_text(yes_data, yes_text, no_data, no_text):
    reply_markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(yes_text, callback_data=yes_data)
    no = types.InlineKeyboardButton(no_text, callback_data=no_data)
    reply_markup.row(yes, no)
    return reply_markup


# Повертає розмітку з кнопками для меню управління даними користувача
def get_personal_data_menu(has_personal_data):
    reply_markup = types.InlineKeyboardMarkup()
    create = types.InlineKeyboardButton('Вписати📝', callback_data=CREATE_PERS_DATA)
    edit = types.InlineKeyboardButton('Редагувати✍️', callback_data=EDIT_PERS_DATA)
    see = types.InlineKeyboardButton('Переглянути👀', callback_data=SEE_PERS_DATA)
    delete = types.InlineKeyboardButton('Видалити🗑', callback_data=REM_PERS_DATA)
    back = types.InlineKeyboardButton('До головного меню◀️', callback_data=MAIN_MENU)
    if has_personal_data:
        reply_markup.row(edit, see)
        reply_markup.row(delete)
        reply_markup.row(back)
    else:
        reply_markup.row(create)
        reply_markup.row(back)
    return reply_markup


# Повертає розмітку з кнопками для головного меню
def get_main_menu():
    reply_markup = types.InlineKeyboardMarkup()
    choose = types.InlineKeyboardButton('Обрати рейс✈️', callback_data=CHOOSE_FLIGHT)
    # ticket_refund = types.InlineKeyboardButton('Повернути квиток↩️', callback_data='/ticket_refund')
    tickets = types.InlineKeyboardButton('Мої квитки🎫', callback_data=TICKETS)
    pers_data = types.InlineKeyboardButton('Персональні дані📁', callback_data=PERSONAL_DATA_MENU)
    support = types.InlineKeyboardButton('Підтримка📞', callback_data=SUPPORT)
    reply_markup.row(choose)
    reply_markup.row(tickets)
    reply_markup.row(pers_data)
    reply_markup.row(support)
    return reply_markup
