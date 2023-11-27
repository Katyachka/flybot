import json
import os

import telebot

import db.db_init as dbmanager
from models.User import User
from service.user_service import UserService
from util.utils import get_personal_data_menu, get_main_menu, START, HELP, MAIN_MENU, PERSONAL_DATA_MENU, SUPPORT, \
    CREATE_PERS_DATA, get_simple_question_marcup, EDIT_GENDER, get_simple_question_marcup_with_text

# Ініціалізація телеграм бот об'єкту
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'), parse_mode='Markdown')

# Ініціалізація бази даних
dbmanager.init_db()


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
    user = UserService.get_user_by_id(User(id=message.chat.id))
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
                     reply_markup=get_simple_question_marcup_with_text(json.dumps({'cmd': EDIT_GENDER, 'val': 'M'}),
                                                                       'Чоловіча👨‍💼',
                                                                       json.dumps({'cmd': EDIT_GENDER, 'val': 'F'}),
                                                                       'Жіноча👩‍💼'))


# Повертає повідомлення з обраною статтю
@bot.callback_query_handler(func=lambda callback: json.loads(callback.data)['cmd'] == EDIT_GENDER)
def edit_gender_callback(callback):
    value = json.loads(callback.data)['val']
    bot.send_message(callback.message.chat.id, value)


# Повертає повідомлення з даних служби підтримки після вибору команди support
@bot.callback_query_handler(func=lambda callback: callback.data == SUPPORT)
def support_callback(callback):
    bot.send_message(callback.message.chat.id, 'Залишились питання?\n'
                                               'Зателефонуйте оператору за номером:\n'
                                               '`+380977070505`')


bot.polling(none_stop=True)
