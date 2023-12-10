import os
import re
import time

import telebot
from telebot.types import LabeledPrice
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

import db.db_init as dbmanager
from models.Flight import Flight
from models.Seat import Seat
from models.SeatModel import SeatModel
from models.Ticket import Ticket
from models.User import User
from models.UserInfo import UserInfo
from models.choose_seat_state import ChooseSeatState
from service.ticket_service import TicketService
from service.chat_cache import ChatCache
from service.flight_service import FlightService
from service.seat_service import SeatService
from service.user_info_service import UserInfoService
from service.user_service import UserService
from service.user_ticket_service import UserTicketService
from util.utils import get_personal_data_menu, get_main_menu, START, HELP, MAIN_MENU, PERSONAL_DATA_MENU, SUPPORT, \
    CREATE_PERS_DATA, EDIT_GENDER, get_simple_question_marcup_with_text, \
    get_save_pers_data_menu, SAVE_PERS_DATA, get_param_from_command, SEE_PERS_DATA, EDIT_PERS_DATA, \
    PRE_SAVE_EDIT_PERS_DATA, get_edit_personal_data_menu, EDIT_NAME, FIELD_NAME, EDIT_SURNAME, FIELD_SURNAME, \
    EDIT_PERS_GENDER, EDIT_GENDER_INTERNAL, FIELD_GENDER, EDIT_PHONE, FIELD_PHONE, EDIT_EMAIL, FIELD_EMAIL, \
    CHOOSE_FLIGHT, get_available_flights_menu, FLIGHT, get_luggage_menu, LUGGAGE, load_photo, get_random_available_seat, \
    generate_seats, SEAT_PAG, CHOOSE_SEAT, OCCUPIED, TICKETS, get_tickets_buttons, \
    get_simple_question_marcup, TICKET

# Ініціалізація телеграм бот об'єкту
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'), parse_mode='Markdown')
provider_token = os.environ.get('STRIPE_API_KEY')

# Ініціалізація бази даних
dbmanager.init_db()

chat_cache = ChatCache()

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
    chat_cache.put_pers_data(callback.message.chat.id, user_info)
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_enter_name)


def on_enter_name(message):
    name = message.text
    user_info = chat_cache.get_pers_data(message.chat.id)

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
    chat_cache.put_pers_data(message.chat.id, user_info)
    bot.send_message(message.chat.id, 'Введіть Ваше прізвище:')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(message, on_enter_surname)


def on_enter_surname(message):
    surname = message.text
    user_info = chat_cache.get_pers_data(message.chat.id)

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
    chat_cache.put_pers_data(message.chat.id, user_info)
    bot.send_message(message.chat.id, 'Введіть Ваш номер телефону в міжнародному форматі (+380):')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(message, on_enter_phone_number)


def on_enter_phone_number(message):
    phone = message.text
    user_info = chat_cache.get_pers_data(message.chat.id)

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
    chat_cache.put_pers_data(message.chat.id, user_info)
    bot.send_message(message.chat.id, 'Введіть Ваш email:')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(message, on_enter_email)


def on_enter_email(message):
    email = message.text
    user_info = chat_cache.get_pers_data(message.chat.id)

    if re.search(email_regex, email):
        user_info.email = email
        chat_cache.put_pers_data(message.chat.id, user_info)
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
        user_info = chat_cache.get_pers_data(callback.message.chat.id)
        id = UserInfoService.create_user(user_info)
        chat_cache.rem_pers_data(callback.message.chat.id)
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
        user_info = chat_cache.get_pers_data(message.chat.id)
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
        chat_cache.put_msg_to_edit(message.chat.id, message_sent.message_id)
    chat_cache.put_msg_to_del(message.chat.id, [])
    to_delete = bot.send_message(message.chat.id, 'Оберіть дані, які хочете редагувати:',
                                 reply_markup=get_edit_personal_data_menu(is_user_saved))
    chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_PERS_DATA)
def edit_personal_data_callback(callback):
    edit_personal_data(callback.message, True, True)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_NAME)
def edit_name_callback(callback):
    to_delete = bot.send_message(callback.message.chat.id, 'Введіть нове ім\'я:')
    chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_edit_name)


def on_edit_name(message):
    name = message.text
    chat_cache.add_msg_to_del(message.chat.id, message.message_id)

    if len(name) < 2:
        to_delete = bot.send_message(message.chat.id, 'Ім\'я повинно складатися хоча б з двох літер. '
                                                             'Спробуйте, будь ласка, ще раз:')
        chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_name)
        return

    if re.search(user_surname_regex, name):
        to_delete = bot.send_message(message.chat.id, 'Ім\'я не повинно містити цифри та спеціальні символи, окрім апострофу. '
                                                      'Спробуйте, будь ласка, ще раз:')
        chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_name)
        return
    edit_field(message, FIELD_NAME, name)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_SURNAME)
def edit_surname_callback(callback):
    to_delete = bot.send_message(callback.message.chat.id, 'Введіть нове прізвище:')
    chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_edit_surname)


def on_edit_surname(message):
    surname = message.text
    chat_cache.add_msg_to_del(message.chat.id, message.message_id)
    if len(surname) < 4:
        to_delete = bot.send_message(message.chat.id, 'Прізвище повинно складатися хоча б з 4 літер. '
                                                             'Спробуйте, будь ласка, ще раз:')
        chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_surname)
        return

    if re.search(user_surname_regex, surname):
        to_delete = bot.send_message(message.chat.id,
                                            'Прізвище не повинно містити цифри та спеціальні символи, окрім апострофу. '
                                            'Спробуйте, будь ласка, ще раз:')
        chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_surname)
        return

    edit_field(message, FIELD_SURNAME, surname)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_PERS_GENDER)
def edit_surname_callback(callback):
    to_delete = bot.send_message(callback.message.chat.id, 'Оберіть стать:',
                                        reply_markup=get_simple_question_marcup_with_text(EDIT_GENDER_INTERNAL + ":M",
                                                                                          'Чоловіча👨‍💼',
                                                                                          EDIT_GENDER_INTERNAL + ":F",
                                                                                          'Жіноча👩‍💼'))
    chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(EDIT_GENDER_INTERNAL))
def edit_gender_internal_callback(callback):
    gender = get_param_from_command(callback.data)
    chat_cache.add_msg_to_del(callback.message.chat.id, callback.message.message_id)
    edit_field(callback.message, FIELD_GENDER, gender)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_PHONE)
def edit_phone_callback(callback):
    to_delete = bot.send_message(callback.message.chat.id, 'Введіть номер телефону:')
    chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_edit_phone)


def on_edit_phone(message):
    phone = message.text
    chat_cache.add_msg_to_del(message.chat.id, message.message_id)

    if len(phone) != 13:
        to_delete = bot.send_message(message.chat.id, 'Номер телефону повинен складатися з 12 цифр та одного символу +. '
                                              'Спробуйте, будь ласка, ще раз:')
        chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_phone)
        return

    if re.search(phone_regex, phone):
        to_delete = bot.send_message(message.chat.id,
                                            'Номер телефону не повинен містити літер або спеціальних символів, окрім +. '
                                            'Спробуйте, будь ласка, ще раз:')
        chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_phone)
        return

    edit_field(message, FIELD_PHONE, phone)


@bot.callback_query_handler(func=lambda callback: callback.data == EDIT_EMAIL)
def edit_email_callback(callback):
    to_delete = bot.send_message(callback.message.chat.id, 'Введіть email:')
    chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
    bot.register_next_step_handler(callback.message, on_edit_email)


def on_edit_email(message):
    email = message.text
    chat_cache.add_msg_to_del(message.chat.id, message.message_id)

    if not re.search(email_regex, email):
        to_delete = bot.send_message(message.chat.id, 'Не валідний email. Спробуйте, будь ласка, ще раз:')
        chat_cache.add_msg_to_del(to_delete.chat.id, to_delete.message_id)
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_edit_email)
        return

    edit_field(message, FIELD_EMAIL, email)


def edit_field(message, field, value):
    try:
        user_info = chat_cache.get_pers_data(message.chat.id)
        setattr(user_info, field, value)
        chat_cache.put_pers_data(message.chat.id, user_info)
        delete_edit_messages(message)
        edit_personal_data(message, False, False)
    except:
        user_info = UserInfoService.get_user_info_by_user_id(message.chat.id)
        setattr(user_info, field, value)
        UserInfoService.update_user(user_info)
        delete_edit_messages(message)
        edit_personal_data(message, False, True)


def delete_edit_messages(message):
    try:
        user_info = chat_cache.get_pers_data(message.chat.id)
    except:
        user_info = UserInfoService.get_user_info_by_user_id(message.chat.id)
    try:
        edit_msg_id = chat_cache.get_msg_to_edit(message.chat.id)
        delete = chat_cache.get_msgs_to_delete(message.chat.id)
        bot.edit_message_text("*Ваші персональні дані:*\n\n"
                              f"*Ім'я*: {user_info.name}\n"
                              f"*Прізвище*: {user_info.surname}\n\n"
                              f"*Стать*: {GENDER[user_info.gender]}\n\n"
                              f"*Номер телефону*: {user_info.phone}\n"
                              f"*Email*: {user_info.email}", message.chat.id, edit_msg_id)
        for rem in delete:
            bot.delete_message(message.chat.id, rem)
        chat_cache.put_msg_to_del(message.chat.id, [])
    except:
        return None


@bot.message_handler(commands=[CHOOSE_FLIGHT])
def choose_flight_handler(message):
    bot.send_message(message.chat.id, 'Введіть,будь ласка, місто відправлення:')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(message, on_enter_city_departure)


@bot.callback_query_handler(func=lambda callback: callback.data == CHOOSE_FLIGHT)
def choose_flight_callback(callback):
    choose_flight_handler(callback.message)


def on_enter_city_departure(message):
    city = message.text

    if len(city) < 2:
        bot.send_message(message.chat.id, 'Назва міста повинна складатися хоча б з двох літер. '
                                          'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_city_departure)
        return

    if re.search(user_surname_regex, city):
        bot.send_message(message.chat.id,
                         'Назва міста не повинна містити цифри та спеціальні символи, окрім апострофу. '
                         'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_city_departure)
        return

    flights_with_city = SeatService.with_available_seats(FlightService.get_with_departure_city(city))

    if flights_with_city:
        chat_cache.put_flight(message.chat.id, Flight(departure=city))
        bot.send_message(message.chat.id, 'Введіть назву міста прибуття:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_city_arrival)
    else:
        bot.send_message(message.chat.id, 'На жаль, рейсів за обраним напрямком не знайдено')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_city_departure)


def on_enter_city_arrival(message):
    city = message.text

    if len(city) < 2:
        bot.send_message(message.chat.id, 'Назва міста повинна складатися хоча б з двох літер. '
                                          'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_city_arrival)
        return

    if re.search(user_surname_regex, city):
        bot.send_message(message.chat.id,
                         'Назва міста не повинна містити цифри та спеціальні символи, окрім апострофу. '
                         'Спробуйте, будь ласка, ще раз:')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_city_arrival)
        return

    flight = chat_cache.get_flight(message.chat.id)
    available_flights = FlightService.get_by_flight(Flight(departure=flight.departure, arrival=city))
    available_flights = SeatService.with_available_seats(available_flights)

    if available_flights:
        flight.arrival = city
        chat_cache.put_flight(message.chat.id, flight)
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.chat.id, f"Оберіть дату: {LSTEP[step]}", reply_markup=calendar)
    else:
        bot.send_message(message.chat.id,
                         f'На жаль, рейсів за обраним напрямком {flight.departure} -> {city} не знайдено...')
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, on_enter_city_arrival)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def select_date_callback(callback):
    result, key, step = DetailedTelegramCalendar().process(callback.data)

    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              callback.message.chat.id,
                              callback.message.message_id,
                              reply_markup=key)
    elif result:
        flight = chat_cache.get_flight(callback.message.chat.id)
        available_flights = FlightService.get_by_flight(Flight(departure=flight.departure, arrival=flight.arrival,
                                                               departure_date_time=result))
        available_flights = SeatService.with_available_seats(available_flights)

        if available_flights:
            bot.send_message(callback.message.chat.id, 'Оберіть рейс:',
                             reply_markup=get_available_flights_menu(available_flights, False))
        else:
            available_flights = FlightService.get_by_flight(Flight(departure=flight.departure, arrival=flight.arrival,
                                                                   departure_date_time=result), False)
            available_flights = SeatService.with_available_seats(available_flights)
            if available_flights:
                bot.send_message(callback.message.chat.id,
                                 'На жаль, на вибрану вами дату рейсів немає.\nНайближчі рейси:',
                                 reply_markup=get_available_flights_menu(available_flights, True))
            else:
                bot.send_message(callback.message.chat.id,
                                 'На жаль, на вибрану вами дату рейсів немає...')


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(FLIGHT))
def flight_callback(callback):
    id = get_param_from_command(callback.data)
    flight = FlightService.get_by_id(id)
    chat_cache.put_flight(callback.message.chat.id, flight)

    chat_cache.put_seat(callback.message.chat.id, Seat(flight_id=id))
    bot.send_message(callback.message.chat.id, '*Оберіть багаж*:\n\n'
                                               'Basic - одна маленька сумка (40х20х25).\n\n'
                                               'Regular - 2 сумки ручної поклажі ( 1 сумка ручної поклажі та одна маленька сумка + Зарезервоване місце.\n\n'
                                               'Plus - 1 маленька сумка + 20 кг багаж + Зарезервоване місце.',
                     reply_markup=get_luggage_menu(flight))


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(LUGGAGE))
def luggage_chosen_callback(callback):
    luggage_type = get_param_from_command(callback.data)
    seat = chat_cache.get_seat(callback.message.chat.id)

    if luggage_type == 'REGULAR':
        seat.luggage_regular = True

    if luggage_type == 'PLUS':
        seat.luggage_plus = True

    chat_cache.put_seat(callback.message.chat.id, seat)
    flight = FlightService.get_by_id(seat.flight_id)

    bot.send_photo(callback.message.chat.id, load_photo(flight.plane.layout))

    if not seat.luggage_regular and not seat.luggage_plus:
        random_seat = get_random_available_seat(flight)
        seat.number = random_seat.number
        chat_cache.put_seat(callback.message.chat.id, seat)
        bot.send_message(callback.message.chat.id, f'Ваше місце: {seat.number}')
    else:
        chat_cache.put_chs_seat_pag_state(callback.message.chat.id, ChooseSeatState(current=1, page_count=18,
                                                                                    flight=flight))
        pag_state = chat_cache.get_chs_seat_pag_state(callback.message.chat.id)
        to_edit = bot.send_message(callback.message.chat.id, 'Оберіть місце відповідно до фотографії:',
                                   reply_markup=pag_state.get_page_btns(generate_seats(flight)))
        chat_cache.put_msg_to_edit(callback.message.chat.id, to_edit.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(SEAT_PAG))
def seat_pagination_callback(callback):
    action = get_param_from_command(callback.data)
    pag_state = chat_cache.get_chs_seat_pag_state(callback.message.chat.id)
    pag_state.apply_action(action)
    chat_cache.put_chs_seat_pag_state(callback.message.chat.id, pag_state)
    edit_msg_id = chat_cache.get_msg_to_edit(callback.message.chat.id)
    flight = chat_cache.get_flight(callback.message.chat.id)
    if pag_state.is_changed():
        bot.edit_message_text('Оберіть місце відповідно до фотографії',
                              callback.message.chat.id, edit_msg_id,
                              reply_markup=pag_state.get_page_btns(generate_seats(flight)))


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(CHOOSE_SEAT))
def choose_seat_callback(callback):
    place_number = get_param_from_command(callback.data)

    if place_number.endswith(OCCUPIED):
        bot.send_message(callback.message.chat.id, 'Вибачте, але це місце вже зайняте, оберіть, будь ласка, інше')
        return

    chat_cache.put_msg_to_edit(callback.message.chat.id, None)
    chat_cache.put_chs_seat_pag_state(callback.message.chat.id, None)
    seat = chat_cache.get_seat(callback.message.chat.id)

    seat.number = place_number

    user = UserService.get_user_by_id(callback.message.chat.id)

    if user.save_info:
        seat.user_info_id = user.user_info_id
        show_pre_buy_data(callback.message)
    else:

        bot.send_message(callback.message.chat.id, 'Hello mather-fucker')

    chat_cache.put_seat(callback.message.chat.id, seat)


def show_pre_buy_data(message):
    seat = chat_cache.get_seat(message.chat.id)

    flight = chat_cache.get_flight(message.chat.id)
    bot.send_message(message.chat.id, "Перегляд бронювання:\n")
    seat_model = SeatModel(number=seat.number, luggage_regular=seat.luggage_regular,
                               luggage_plus=seat.luggage_plus, flight=flight)
    luggage = 'Ручна поклажа'
    cost = flight.cost_base

    if seat.luggage_regular:
        luggage = '2 сумки ручної поклажі (1 сумка ручної поклажі та одна маленька сумка)'
        cost += flight.cost_regular

    if seat.luggage_plus:
        luggage = '1 маленька сумка + 20 кг багаж'
        cost += flight.cost_plus

    show_ticket_info(seat_model, message)

    bot.send_invoice(message.chat.id,
                     title='Оплата квитків',
                     description=f'Рейс: {flight.departure} {flight.departure_date_time.strftime("%d.%m.%Y %H:%M")} '
                                 f'-> {flight.arrival} {flight.arrival_date_time.strftime("%d.%m.%Y %H:%M")}',
                     currency='usd',
                     prices=[LabeledPrice(label=f'Квиток: {seat.number}, багаж: {luggage}', amount=int(cost)*100)],
                     provider_token=provider_token,
                     is_flexible=False,
                     invoice_payload='FlyBot')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Інопланетяни намагалися викрасти CVV вашої картки, але ми успішно захистили ваші облікові дані, "
                                                 " Спробуйте оплатити ще раз через кілька хвилин, нам потрібен невеликий відпочинок.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    seat = chat_cache.get_seat(message.chat.id)
    flight = chat_cache.get_flight(message.chat.id)
    seat.id = SeatService.create_seat(seat)
    ticket = Ticket(plane_id=flight.plane.id, flight_id=flight.id, seat_id=seat.id)
    ticket.id = TicketService.create_ticket(ticket)
    user = UserService.get_user_by_id(message.chat.id)
    UserTicketService.create_user_ticket(user, ticket)

    chat_cache.put_seat(message.chat.id, None)
    chat_cache.put_flight(message.chat.id, None)
    chat_cache.put_chs_seat_pag_state(message.chat.id, None)
    chat_cache.put_msg_to_edit(message.chat.id, None)

    bot.send_message(message.chat.id,
                     "Дякуємо за оплату! Ми виконаємо ваше замовлення на `{} {}` якомога швидше! "
                      "Залишайтеся на зв’язку.".format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


@bot.message_handler(commands=[TICKETS])
def tickets_handler(message):
    tickets = UserTicketService.get_user_tickets(message.chat.id)
    if tickets:
        reply_marcup = get_tickets_buttons(tickets)
        bot.send_message(message.chat.id, 'Оберіть квиток:', reply_markup=reply_marcup)
    else:
        bot.send_message(message.chat.id, 'На жаль, ви ще не придбали жодних квитків. Бажаєте обрати рейс?',
                         reply_markup=get_simple_question_marcup(CHOOSE_FLIGHT, MAIN_MENU))


@bot.callback_query_handler(func=lambda callback: callback.data == TICKETS)
def tickets_callback(callback):
    tickets_handler(callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(TICKET))
def ticket_callback(callback):
    ticket_id = get_param_from_command(callback.data)
    ticket = TicketService.get_ticket(ticket_id)
    seat = SeatService.get_by_id(ticket.seat_id)
    show_ticket_info(seat, callback.message)


def show_ticket_info(seat, message):
    bot.send_message(message.chat.id, f"Рейс: {seat.flight.departure} -> {seat.flight.arrival}\n\n"
                                      f"Дата та час відправлення: {seat.flight.departure_date_time.strftime("%d.%m.%Y %H:%M")}\n"
                                      f"Дата та час прибуття: {seat.flight.arrival_date_time.strftime("%d.%m.%Y %H:%M")}\n"
                                      f"Тривалість польоту: {seat.flight.duration} год.\n\n"
                                      f"Літак: {seat.flight.plane.model}\n\n")

    bot.send_photo(message.chat.id, load_photo(seat.flight.plane.layout))

    luggage = 'Ручна поклажа'
    cost = seat.flight.cost_base

    if seat.luggage_regular:
        luggage = '2 сумки ручної поклажі (1 сумка ручної поклажі та одна маленька сумка)'
        cost += seat.flight.cost_regular

    if seat.luggage_plus:
        luggage = '1 маленька сумка + 20 кг багаж'
        cost += seat.flight.cost_plus

    bot.send_message(message.chat.id, f"Ваше місце: {seat.number}\n"
                                      f"Багаж: {luggage}")
    see_personal_data(message)


@bot.message_handler(commands=[SUPPORT])
def support_handler(message):
    bot.send_message(message.chat.id, 'Залишились питання?\n'
                                      'Зателефонуйте оператору за номером:\n'
                                      '`+380977070505`')


@bot.callback_query_handler(func=lambda callback: callback.data == SUPPORT)
def support_callback(callback):
    support_handler(callback.message)


bot.polling(none_stop=True)
