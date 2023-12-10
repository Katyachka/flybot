import os
import random
from math import ceil

from telebot import types

from models.Flight import Flight
from models.FlightModel import FlightModel
from models.Seat import Seat
from service.flight_service import FlightService
from service.seat_service import SeatService

# Константи з командами
START = 'start'
HELP = 'help'
PERSONAL_DATA_MENU = 'pers_data_menu'
MAIN_MENU = 'main_menu'
CHOOSE_FLIGHT = 'choose_flight'
TICKETS = 'tickets'
TICKET = 'my_ticket'
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
FLIGHT = 'flight'
LUGGAGE = 'luggage'
CHOOSE_SEAT = 'choose_seat'
SEAT_PAG = "pag_seats"
PAY = "pay"

CMD = 'cmd'
DATA = 'data'

OCCUPIED = "occupied"

NEXT = "++"
PREV = "--"

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


def get_available_flights_menu(available_flight, with_dates):
    reply_markup = types.InlineKeyboardMarkup()
    for flight in available_flight:
        reply_markup.row(types.InlineKeyboardButton(f"{get_flight_btn_text(flight, with_dates)}",
                                                    callback_data=f"{FLIGHT}:{flight.id}"))
    return reply_markup


def get_flight_btn_text(flight: Flight, with_date):
    if with_date:
        text = f"{flight.departure_date_time.strftime("%d.%m.%Y (%H:%M)")} -> {flight.arrival_date_time.strftime("%d.%m.%Y (%H:%M)")}"
    else:
        dep_time = f"{flight.departure_date_time.hour}:{flight.departure_date_time.minute}"
        arr_time = f"{flight.arrival_date_time.hour}:{flight.arrival_date_time.minute}"
        text = f"{dep_time} -> {arr_time}"
    return text


def get_luggage_menu(flight: Flight):
    reply_markup = types.InlineKeyboardMarkup()
    base = types.InlineKeyboardButton(f'Basic - {flight.cost_base}$', callback_data=f"{LUGGAGE}:BASE")
    regular = types.InlineKeyboardButton(f'Regular - {flight.cost_base}$ + {flight.cost_regular}$',
                                         callback_data=f"{LUGGAGE}:REGULAR")
    plus = types.InlineKeyboardButton(f'Plus - {flight.cost_base}$ + {flight.cost_plus}$',
                                      callback_data=f"{LUGGAGE}:PLUS")
    reply_markup.row(base, regular)
    reply_markup.row(plus)
    return reply_markup


def get_param_from_command(command):
    path = command.split(':')
    return path[len(path) - 1]


def load_photo(filename):
    relative_photo_path = f'./layout/{filename}'

    absolute_photo_path = os.path.abspath(relative_photo_path)

    if os.path.exists(absolute_photo_path):
        return open(absolute_photo_path, 'rb')
    else:
        return None


def generate_seats(flight: FlightModel):
    result = []
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    seats = SeatService.get_all_by_flight_id(flight.id)
    for i in range(ceil(flight.plane.passengers / flight.plane.seat_in_row)):
        for letter in letters:
            number = f"{i + 1}{letter}"
            if any(val.number == number for val in seats):
                number = f"{number} (вже зайняте)"
            seat = Seat(flight_id=flight.id, number=number)
            result.append(seat)
    return result


def get_random_available_seat(flight: FlightModel):
    result = []
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    seats = SeatService.get_all_by_flight_id(flight.id)
    for i in range(ceil(flight.plane.passengers / flight.plane.seat_in_row)):
        for letter in letters:
            number = f"{i}{letter}"
            if any(val.number == number for val in seats):
                continue
            seat = Seat(flight_id=flight.id, number=number)
            result.append(seat)
    seat_index = random.randint(0, len(result) - 1)
    return result[seat_index]


def get_tickets_buttons(tickets: list):
    reply_markup = types.InlineKeyboardMarkup()
    for ticket in tickets:
        flight = FlightService.get_by_id(ticket.flight_id)
        reply_markup.row(types.InlineKeyboardButton(f"{flight.departure} -> {flight.arrival}", callback_data=f"{TICKET}:{ticket.id}"))
    reply_markup.row(types.InlineKeyboardButton('До головного меню◀️', callback_data=MAIN_MENU))
    return reply_markup

