import os
import re
import time

import telebot

import db.db_init as dbmanager
from models.User import User
from models.UserInfo import UserInfo
from service.user_info_service import UserInfoService
from service.user_service import UserService
from util.utils import get_personal_data_menu, get_main_menu, START, HELP, MAIN_MENU, PERSONAL_DATA_MENU, SUPPORT, \
    CREATE_PERS_DATA, EDIT_GENDER, get_simple_question_marcup_with_text, \
    get_save_pers_data_menu, SAVE_PERS_DATA, get_param_from_command, SEE_PERS_DATA, EDIT_PERS_DATA, \
    PRE_SAVE_EDIT_PERS_DATA, get_edit_personal_data_menu, EDIT_NAME, FIELD_NAME, EDIT_SURNAME, FIELD_SURNAME, \
    EDIT_PERS_GENDER, EDIT_GENDER_INTERNAL, FIELD_GENDER, EDIT_PHONE, FIELD_PHONE, EDIT_EMAIL, FIELD_EMAIL

# Ініціалізація телеграм бот об'єкту
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'), parse_mode='Markdown')

# Ініціалізація бази даних
dbmanager.init_db()

personal_data = {}
message_to_edit = {}
messages_to_delete = {}


user_surname_regex = "[0-9!@#$%^&()_+=\*\-~`{}\[\]:;\",\.?/\\|<>№]+"
phone_regex = "[a-zA-Zа-яА-ЯІіЇїЄ!@#$%^&()_=\*\-~'`{}\[\]:;\",\.?/\\|<>№]+"
email_regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

GENDER = {
    'M': 'Чоловік',
    'F': 'Жінка'
}


# Повертає повідомлення з привітанням після команди start
@bot.message_handler(commands=[START])
def send_welcome(message):
    bot.send_message(message.chat.id, f'{message.chat.first_name}, вітаємо Вас у Flying бот. Цей бот допоможе Вам '
                                      f'придбати авіаквитки✈️')
    main_menu(message)


# Повертає повідомлення з головними командами бота
@bot.message_handler(commands=[HELP])
def send_help(message):
    bot.send_message(message.chat.id, 'Цей бот містить такі команди: \n'
                                      '/start - почати використовувати бот\n'
                                      '/help - перелік команд, які містить в собі бот\n')


# Повертає повідомлення з кнопками головного меню
@bot.message_handler(commands=[MAIN_MENU])
def main_menu(message):
    bot.send_message(message.chat.id, 'Оберіть, що хочете зробити🎮', reply_markup=get_main_menu())


# Повертає повідомлення з кнопками головного меню
@bot.callback_query_handler(func=lambda callback: callback.data == MAIN_MENU)
def main_menu_callback(callback):
    main_menu(callback.message)


# Пропонує зберегти персональні дані або показує меню персональних даних
@bot.message_handler(commands=[PERSONAL_DATA_MENU])
def personal_data_menu(message):
    user = UserService.get_user_by_id(message.chat.id)
    if user is not None and user.save_info:
        bot.send_message(message.chat.id, 'Оберіть дію з персональними даними:',
                         reply_markup=get_personal_data_menu(True))
    else:
        bot.send_message(message.chat.id,
                         'Ви можете зберегти персональні дані, щоб не вводити їх при наступній купівлі квитків📥',
                         reply_markup=get_personal_data_menu(False))


# Показує меню особистих даних
@bot.callback_query_handler(func=lambda callback: callback.data == PERSONAL_DATA_MENU)
def personal_data_callback(callback):
    personal_data_menu(callback.message)


# Повертає повідомлення з кнопками вибору статі
@bot.callback_query_handler(func=lambda callback: callback.data == CREATE_PERS_DATA)
def create_pers_data_callback(callback):
    bot.send_message(callback.message.chat.id, 'Оберіть, будь ласка, стать:',
                     reply_markup=get_simple_question_marcup_with_text(EDIT_GENDER + ":M", 'Чоловіча👨‍💼',
                                                                       EDIT_GENDER + ":F", 'Жіноча👩‍💼'))


#
@bot.callback_query_handler(func=lambda callback: callback.data.startswith(EDIT_GENDER))
def edit_gender_callback(callback):
    gender = get_param_from_command(callback.data)
    bot.send_message(callback.message.chat.id, 'Введіть Ваше ім\'я:')
    user_info = UserInfo(gender=gender)
    personal_data[callback.message.chat.id] = user_info
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_enter_name)


def on_enter_name(message):
    name = message.text
    user_info = personal_data[message.chat.id]

    if len(name) < 2:
        bot.send_message(message.chat.id, 'Ім\'я повинно складатися хоча б з двох літер. '
                                          'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_name)
        return

    if re.search(user_surname_regex, name):
        bot.send_message(message.chat.id, 'Ім\'я не повинно містити цифри та спеціальні символи, окрім апострофу. '
                                          'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_name)
        return

    user_info.name = name
    personal_data[message.chat.id] = user_info
    bot.send_message(message.chat.id, 'Введіть Ваше прізвище:')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(message, on_enter_surname)


def on_enter_surname(message):
    surname = message.text
    user_info = personal_data[message.chat.id]

    if len(surname) < 4:
        bot.send_message(message.chat.id, 'Прізвище повинно складатися хоча б з 4 літер. '
                                          'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_surname)
        return

    if re.search(user_surname_regex, surname):
        bot.send_message(message.chat.id, 'Прізвище не повинно містити цифри та спеціальні символи, окрім апострофу. '
                                          'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_surname)
        return

    user_info.surname = surname
    personal_data[message.chat.id] = user_info
    bot.send_message(message.chat.id, 'Введіть Ваш номер телефону в міжнародному форматі (+380):')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(message, on_enter_phone_number)


def on_enter_phone_number(message):
    phone = message.text
    user_info = personal_data[message.chat.id]

    if len(phone) != 13:
        bot.send_message(message.chat.id, 'Номер телефону повинен складатися з 12 цифр та одного символу +. '
                                          'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_phone_number)
        return

    if re.search(phone_regex, phone):
        bot.send_message(message.chat.id, 'Номер телефону не повинен містити літер або спеціальних символів, окрім +. '
                                          'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_phone_number)
        return

    user_info.phone = phone
    personal_data[message.chat.id] = user_info
    bot.send_message(message.chat.id, 'Введіть Ваш email:')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(message, on_enter_email)


def on_enter_email(message):
    email = message.text
    user_info = personal_data[message.chat.id]

    if re.search(email_regex, email):
        user_info.email = email
        personal_data[message.chat.id] = user_info
        bot.send_message(message.chat.id, 'Ви ввели наступні дані:\n')
        bot.send_message(message.chat.id, f"*Ім'я*: {user_info.name}\n"
                                          f"*Прізвище*: {user_info.surname}\n\n"
                                          f"*Стать*: {GENDER[user_info.gender]}\n\n"
                                          f"*Номер телефону*: {user_info.phone}\n"
                                          f"*Email*: {user_info.email}")
        bot.send_message(message.chat.id, 'Оберіть дію: ', reply_markup=get_save_pers_data_menu())
    else:
        bot.send_message(message.chat.id, 'Не валідний email. Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_email)


@bot.callback_query_handler(func=lambda callback: callback.data == PRE_SAVE_EDIT_PERS_DATA)
def pre_save_menu_handler(callback):
    bot.send_message(callback.message.chat.id, 'Оберіть дію: ', reply_markup=get_save_pers_data_menu())


@bot.callback_query_handler(func=lambda callback: callback.data == SAVE_PERS_DATA)
def save_pers_info_callback(callback):
    try:
        user_info = personal_data[callback.message.chat.id]
        id = UserInfoService.create_user(user_info)
        del personal_data[callback.message.chat.id]
        user = User(id=callback.message.chat.id, user_info_id=id, save_info=True)
        UserService.create_user(user)
        bot.send_message(callback.message.chat.id, "Ваші персональні дані успішно збережені. 🎉🎉🎉")
        time.sleep(2)
        main_menu(callback.message)
    except:
        bot.send_message(callback.message.chat.id, "Упс, щось пішло не так, ми над цим працюємо...")


@bot.callback_query_handler(func=lambda callback: callback.data == SEE_PERS_DATA)
def see_personal_data_callback(callback):
    see_personal_data(callback.message)


def see_personal_data(message):
    try:
        user_info = personal_data[message.chat.id]
    except:
        user_info = UserInfoService.get_user_info_by_user_id(message.chat.id)
    return bot.send_message(message.chat.id, "*Ваші персональні дані:*\n\n"
                                      f"*Ім'я*: {user_info.name}\n"
                                      f"*Прізвище*: {user_info.surname}\n\n"
                                      f"*Стать*: {GENDER[user_info.gender]}\n\n"
                                      f"*Номер телефону*: {user_info.phone}\n"
                                      f"*Email*: {user_info.email}")


def edit_personal_data(message, show, is_user_saved):
    if show:
        message_sent = see_personal_data(message)
        message_to_edit[message.chat.id] = message_sent.message_id
    messages_to_delete[message.chat.id] = []
    add_delete_message(bot.send_message(message.chat.id, 'Оберіть дані, які хочете редагувати:',
                                                                reply_markup=get_edit_personal_data_menu(is_user_saved)))


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_PERS_DATA)
def edit_personal_data_callback(callback):
    edit_personal_data(callback.message, True, True)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_NAME)
def edit_name_callback(callback):
    add_delete_message(bot.send_message(callback.message.chat.id, 'Введіть нове ім\'я:'))
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_edit_name)


def on_edit_name(message):
    name = message.text
    add_delete_message(message)

    if len(name) < 2:
        add_delete_message(bot.send_message(message.chat.id, 'Ім\'я повинно складатися хоча б з двох літер. '
                                          'Спробуйте, будь ласка, ще раз:'))
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_name)
        return

    if re.search(user_surname_regex, name):
        add_delete_message(bot.send_message(message.chat.id, 'Ім\'я не повинно містити цифри та спеціальні символи, окрім апострофу. '
                                          'Спробуйте, будь ласка, ще раз:'))
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_name)
        return
    edit_field(message, FIELD_NAME, name)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_SURNAME)
def edit_surname_callback(callback):
    add_delete_message(bot.send_message(callback.message.chat.id, 'Введіть нове прізвище:'))
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_edit_surname)


def on_edit_surname(message):
    surname = message.text
    add_delete_message(message)

    if len(surname) < 4:
        add_delete_message(bot.send_message(message.chat.id, 'Прізвище повинно складатися хоча б з 4 літер. '
                                          'Спробуйте, будь ласка, ще раз:'))
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_surname)
        return

    if re.search(user_surname_regex, surname):
        add_delete_message(bot.send_message(message.chat.id, 'Прізвище не повинно містити цифри та спеціальні символи, окрім апострофу. '
                                          'Спробуйте, будь ласка, ще раз:'))
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_surname)
        return

    edit_field(message, FIELD_SURNAME, surname)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_PERS_GENDER)
def edit_surname_callback(callback):
    add_delete_message(bot.send_message(callback.message.chat.id, 'Оберіть стать:',
                                        reply_markup=get_simple_question_marcup_with_text(EDIT_GENDER_INTERNAL + ":M", 'Чоловіча👨‍💼',
                                                                                          EDIT_GENDER_INTERNAL + ":F", 'Жіноча👩‍💼')))


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(EDIT_GENDER_INTERNAL))
def edit_gender_internal_callback(callback):
    gender = get_param_from_command(callback.data)
    add_delete_message(callback.message)
    edit_field(callback.message, FIELD_GENDER, gender)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_PHONE)
def edit_phone_callback(callback):
    add_delete_message(bot.send_message(callback.message.chat.id, 'Введіть номер телефону:'))
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_edit_phone)


def on_edit_phone(message):
    phone = message.text
    add_delete_message(message)

    if len(phone) != 13:
        add_delete_message(bot.send_message(message.chat.id, 'Номер телефону повинен складатися з 12 цифр та одного символу +. '
                                          'Спробуйте, будь ласка, ще раз:'))
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_phone)
        return

    if re.search(phone_regex, phone):
        add_delete_message(bot.send_message(message.chat.id, 'Номер телефону не повинен містити літер або спеціальних символів, окрім +. '
                                          'Спробуйте, будь ласка, ще раз:'))
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_phone)
        return

    edit_field(message, FIELD_PHONE, phone)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_EMAIL)
def edit_email_callback(callback):
    add_delete_message(bot.send_message(callback.message.chat.id, 'Введіть email:'))
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_edit_email)


def on_edit_email(message):
    email = message.text
    add_delete_message(message)

    if not re.search(email_regex, email):
        add_delete_message(bot.send_message(message.chat.id, 'Не валідний email. Спробуйте, будь ласка, ще раз:'))
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_email)
        return

    edit_field(message, FIELD_EMAIL, email)


def edit_field(message, field, value):
    try:
        user_info = personal_data[message.chat.id]
        setattr(user_info, field, value)
        personal_data[message.chat.id] = user_info
        delete_edit_messages(message)
        edit_personal_data(message, False, False)
    except:
        user_info = UserInfoService.get_user_info_by_user_id(message.chat.id)
        setattr(user_info, field, value)
        UserInfoService.update_user(user_info)
        delete_edit_messages(message)
        edit_personal_data(message, False, True)


def add_delete_message(message):
    messages_to_delete[message.chat.id].append(message.message_id)


def delete_edit_messages(message):
    try :
        user_info = personal_data[message.chat.id]
    except:
        user_info = UserInfoService.get_user_info_by_user_id(message.chat.id)
    try:
        edit_msg_id = message_to_edit[message.chat.id]
        delete = messages_to_delete[message.chat.id]
        bot.edit_message_text("*Ваші персональні дані:*\n\n"
                              f"*Ім'я*: {user_info.name}\n"
                              f"*Прізвище*: {user_info.surname}\n\n"
                              f"*Стать*: {GENDER[user_info.gender]}\n\n"
                              f"*Номер телефону*: {user_info.phone}\n"
                              f"*Email*: {user_info.email}", message.chat.id, edit_msg_id)
        for rem in delete:
            bot.delete_message(message.chat.id, rem)
        del messages_to_delete[message.chat.id]
        messages_to_delete[message.chat.id] = []
    except:
        return None


@bot.callback_query_handler(func=lambda callback: callback.data == SUPPORT)
def support_callback(callback):
    bot.send_message(callback.message.chat.id, 'Залишились питання?\n'
                                               'Зателефонуйте оператору за номером:\n'
                                               '`+380977070505`')


bot.polling(none_stop=True)
