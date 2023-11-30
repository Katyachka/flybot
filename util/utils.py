
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
EDIT_NAME = 'pers_data_edit_name'
EDIT_SURNAME = 'pers_data_edit_surname'
EDIT_PERS_GENDER = 'pers_data_edit_gender'
EDIT_PHONE = 'pers_data_edit_phone'
EDIT_EMAIL = 'pers_data_edit_email'
EDIT_GENDER = 'edit_gender'
EDIT_GENDER_INTERNAL = "change_gender"
SAVE_PERS_DATA = 'save_pers_data'
PRE_SAVE_EDIT_PERS_DATA = 'pre_save_edit_pers_data'


CMD = 'cmd'
DATA = 'data'

FIELD_NAME = "name"
FIELD_SURNAME = "surname"
FIELD_GENDER = "gender"
FIELD_PHONE = "phone"
FIELD_EMAIL = "email"


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


def get_save_pers_data_menu():
    reply_markup = types.InlineKeyboardMarkup()
    save = types.InlineKeyboardButton('Зберегти💾', callback_data=SAVE_PERS_DATA)
    edit = types.InlineKeyboardButton('Редагувати✍️', callback_data=EDIT_PERS_DATA)
    cancel = types.InlineKeyboardButton('Відмінити❌', callback_data=MAIN_MENU)
    reply_markup.row(save, edit)
    reply_markup.row(cancel)
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


def get_edit_personal_data_menu(flag):
    reply_markup = types.InlineKeyboardMarkup()
    name = types.InlineKeyboardButton('Ім\'я', callback_data=EDIT_NAME)
    surname = types.InlineKeyboardButton('Прізвище', callback_data=EDIT_SURNAME)
    gender = types.InlineKeyboardButton('Стать', callback_data=EDIT_PERS_GENDER)
    phone = types.InlineKeyboardButton('Номер телефону', callback_data=EDIT_PHONE)
    email = types.InlineKeyboardButton('Email', callback_data=EDIT_EMAIL)
    back_to_personal_menu = types.InlineKeyboardButton('Назад◀️', callback_data=PERSONAL_DATA_MENU)
    back_to_personal_save_menu = types.InlineKeyboardButton('Назад◀️', callback_data=PRE_SAVE_EDIT_PERS_DATA)
    reply_markup.row(name, surname)
    reply_markup.row(gender, phone)
    reply_markup.row(email)
    if flag:
        reply_markup.row(back_to_personal_menu)
    else:
        reply_markup.row(back_to_personal_save_menu)
    return reply_markup


def get_param_from_command(command):
    path = command.split(':')
    return path[len(path) - 1]