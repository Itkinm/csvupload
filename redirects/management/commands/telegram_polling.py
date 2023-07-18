import requests

import telebot
from telebot import types
import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from redirects.utils.csv_utils import upload_csv
from redirects.utils.auth_utils import make_auth_url, register, check_registration

token = settings.TOKEN
bot = telebot.TeleBot(token)
bot.send_message(95856961, 'restarted')


def download_csv(message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file_info = bot.get_file(file_id)
    file_path = '/' + file_name
    URL = 'https://api.telegram.org/file/bot{0}/{1}'
    thefile = requests.get(URL.format(token, file_info.file_path))
    with open(file_name, 'wb') as write:
        write.write(thefile.content)

    return file_name


def send_auth_link(message):
    auth_url = make_auth_url('tg_id'+str(message.from_user.id))
        
    markup = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton(text = 'Google Login', 
                                       url = auth_url)
    markup.add(itembtn)
    bot.send_message(message.chat.id, 
                     'This is the bot, gimme access', 
                     reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    if message.text == '/start':
        send_auth_link(message)
    elif message.text[7:] == str(message.from_user.id):
        register(message.from_user.id)
        bot.send_message(message.chat.id, "You are authorized, can send csvs now")
    else:
        bot.send_message(message.chat.id, "There is a problem with authorization")


@bot.message_handler(content_types=["document"],
    func=lambda message: message.document.file_name.endswith(".csv"))
def answer_messages(message):
    if check_registration(message.from_user.id):
        file_name = download_csv(message)
        sh = upload_csv(file_name, message.from_user.id)
        bot.send_message(message.chat.id, sh.url)
    else:
        send_auth_link(message)


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.polling(none_stop=True)