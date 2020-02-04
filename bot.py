# -*- coding: utf-8 -*-
'''
Module for interacting with Telegram API
https://core.telegram.org/bots/api
using pyTelegramBotAPI
https://github.com/eternnoir/pyTelegramBotAPI
Implemented recording of message history using the csv module.
'''

from telebot import TeleBot, apihelper, types
from youtube_parse import get_audio, get_info, get_video

import csv
from datetime import datetime
import logging
import os

from config import token


logging.basicConfig(filename='log.txt', level=logging.WARNING,
                    format='%(asctime)s - %(name)s - \
                    %(levelname)s - %(message)s')

bot = TeleBot(token)
remove_keyboard = types.ReplyKeyboardRemove()
url = ''


def write_csv(message):
    '''Write history to csv-file.'''
    with open(os.getcwd() + '/history.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow((int(message.message_id/2),
        time.strftime("%d.%m.%Y %H:%M:%S"), message.from_user.first_name,
        message.from_user.last_name, message.from_user.id, message.text))


def log(message):
    '''Print log output to the console.'''
    global url
    url = ''
    print("\n ------")
    print("", time.strftime("%d.%m.%Y %H:%M:%S"))
    print(" Сообщение от {first_name} {last_name}.".format(
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name))
    print(" id = {user_id}".format(user_id=str(message.from_user.id)))
    print(" Текст = {message_text}".format(message_text=message.text))
    print(" Всего боту было отправлено {count_message} сообщений \n".format(
        count_message=int(message.message_id/2)))
    
    
def error_message(message):
    global url
    url = ''
    bot.send_message(
        message.chat.id, 'An unexpected error occurred. \
                        Repeat request.', reply_markup=remove_keyboard)
    log(message)
    for f in os.listdir('data'):
        os.remove(os.getcwd() + '/data/' + f)
    url = ''
    
    
def send_file(**kwarg):
    files = os.listdir('data')
    file_name = files[0]
    try:
        with open('data/' + file_name, 'rb') as file:
            if kwarg['params'] == 'send_voice':
                bot.send_voice(kwarg['message_chat_id'], file)
            elif kwarg['params'] == 'send_document':
                bot.send_video(kwarg['message_chat_id'], file)
    except:
        bot.send_message(kwarg['message_chat_id'], 'An error occurred \
                                while file was sending. Repeat request.',
                         reply_markup=remove_keyboard)
    finally:
        url = ''
        for f in files:
            os.remove(os.getcwd() + '/data/' + f)


@bot.message_handler(regexp='youtube.com/\D|youtu.be/')
def get_info_from_link(message):
    global url
    log(message)
    write_csv(message)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, 
                                       resize_keyboard=False)
    markup.add('audio')
    try:
        for item in get_info(url=message.text, params='check_info'):
            markup.add(item)
            bot.send_message(message.chat.id, "Choose one quality:", 
                                        reply_markup=markup)
        url = message.text
    except:
        error_message(message)


@bot.message_handler(regexp='\d\d\dp\d\d|audio')
def set_quality(message):
    global url
    write_csv(message)
    if message.text == "audio" and url != '':
        bot.send_message(message.chat.id, "Just a second, please", 
                                    reply_markup=remove_keyboard)
        try:
            get_audio(url)
            send_file(message_chat_id = message.chat.id, params='send_voice')
        except:
            url = ''
            error_message(message)
    else:
        info = message.text.split('p')
        if get_info(url=url, params='check_filesize', 
            height=int(info[0]), fps=int(info[1])) == True and url != '':
            bot.send_message(message.chat.id, "Just a second, please",
                                    reply_markup=remove_keyboard)
            try:
                get_video(url, info[0], info[1])
                url = ''
                send_file(message_chat_id=message.chat.id, 
                          params='send_document')
            except:
                url = ''
                error_message(message)
        else:
            url = ''
            bot.send_message(message.chat.id, 'Sorry. Your file \
            is very large(500+ MB)', reply_markup=remove_keyboard)


@bot.message_handler(func=lambda message: True, content_types=['audio', 
        'video', 'document', 'text', 'location', 'contact', 'sticker'])
def incorrect_message(message):
    write_csv(message)
    log(message)
    bot.send_message(
        message.chat.id, 'Invalid URL. Correct and \
        retry the request', reply_markup=remove_keyboard)
    try:
        for f in os.listdir('data'):
        os.remove(os.getcwd() + '/data/' + f)
    except:
        pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
