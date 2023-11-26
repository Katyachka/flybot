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


@bot.message_handler(commands=[START])
def send_welcome(message):
    bot.send_message(message.chat.id, f'{message.chat.first_name}, вітаємо Вас у Flying бот. Цей бот допоможе Вам '
                                      f'придбати авіаквитки✈️')
    main_menu(message)


@bot.message_handler(commands=[HELP])
def send_help(message):
    bot.send_message(message.chat.id, 'Цей бот містить такі команди: \n'
                                            '/start - почати використовувати бот\n'
                                            '/help - перелік команд, які містить в собі бот\n')


@bot.message_handler(commands=[MAIN_MENU])
def main_menu(message):
    bot.send_message(message.chat.id, 'Оберіть, що хочете зробити🎮', reply_markup=get_main_menu())


@bot.message_handler(commands=[PERSONAL_DATA_MENU])
def personal_data_menu(message):
    user = UserService.get_user_by_id(User(id=message.chat.id))
    if user is None:
        bot.send_message(message.chat.id, 'Ви можете зберегти персональні дані, щоб не вводити їх при наступній купівлі квитків📥',
                         reply_markup=get_personal_data_menu(False))
    else:
        bot.send_message(message.chat.id, 'Оберіть дію з персональними даними:',
                         reply_markup=get_personal_data_menu(True))


@bot.callback_query_handler(func=lambda callback: callback.data == PERSONAL_DATA_MENU)
def personal_data_callback(callback):
    personal_data_menu(callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data == CREATE_PERS_DATA)
def create_pers_data_callback(callback):
    bot.send_message(callback.message.chat.id, 'Оберіть, будь ласка, стать:',
                     reply_markup=get_simple_question_marcup_with_text(json.dumps({'cmd': EDIT_GENDER, 'val': 'M'}),
                                                                       'Чоловіча👨‍💼',
                                                                       json.dumps({'cmd': EDIT_GENDER, 'val': 'F'}),
                                                                       'Жіноча👩‍💼'))


@bot.callback_query_handler(func=lambda callback: json.loads(callback.data)['cmd'] == EDIT_GENDER)
def edit_gender_callback(callback):
    value = json.loads(callback.data)['val']
    bot.send_message(callback.message.chat.id, value)


@bot.callback_query_handler(func=lambda callback: callback.data == SUPPORT)
def support_callback(callback):
    bot.send_message(callback.message.chat.id, 'Залишились питання?\n'
                                               'Зателефонуйте оператору за номером:\n'
                                               '`+380977070505`')


bot.polling(none_stop=True)
