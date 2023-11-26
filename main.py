import os

import telebot
from telebot import types

import db.db_init as dbmanager
from util.utils import get_personal_data_menu, get_main_menu, START, HELP, MAIN_MENU, PERSONAL_DATA_MENU, SUPPORT

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
    bot.send_message(message.chat.id, 'Оберіть дію з персональними даними', reply_markup=get_personal_data_menu(message.chat.id))


@bot.callback_query_handler(func= lambda callback: callback.data == PERSONAL_DATA_MENU)
def personal_data_callback(callback):
    personal_data_menu(callback.message)


@bot.callback_query_handler(func= lambda callback: callback.data == SUPPORT)
def support_callback(callback):
    bot.send_message(callback.message.chat.id, 'Залишились питання?\n'
                                               'Зателефонуйте оператору за номером:\n'
                                               '`+380977070505`')


bot.polling(none_stop=True)
