import os

import telebot
from telebot import types

# Ініціалізація телеграм бот об'єкту
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'{message.chat.first_name}, вітаємо Вас у Flying бот. Цей бот допоможе Вам '
                                      f'придбати авіаквитки✈️')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Цей бот містить такі команди: \n'
                                            '/start - почати використовувати бот\n'
                                            '/help - перелік команд, які містить в собі бот\n')


bot.polling(none_stop=True)
