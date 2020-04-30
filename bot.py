# vk_session = vk_api.VkApi(token='7da878b295b0d058604a46bc0781ca269051d5c78dd780fe9aa85b2b49d89b9f51698d1eaf22d66684e32')
# da878b295b0d058604a46bc0781ca269051d5c78dd780fe9aa85b2b49d89b9f51698d1eaf22d66684e32
# 1078999841:AAF4MoPFmMAMMC-nO7amyhmTTLLnRElDOR4
#from distutils.command.config import config

import telebot
import config
import random
import http.cookiejar
import requests
import json

from bs4 import BeautifulSoup as BS

from telebot import types

### Парсер
KeysOfPlays = []
ValueOfResaults = []
SumBet = 0
Link = ""
Bets = []
SumBets = 0
datefirst = ""
####### cookie
cookie = {
    "__cfduid": "d05215d9087bd1c4bedc6c712fd423c8a1585849850",
    "express.sid": "s%3Ar0yi7P4wIkj1jdkO_zexh1fIjlKMnI6x.6JPXTM10YeiZHbOVOM%2BmlXvDeAO3Ebh1S8Ya3WY%2BiCM",
    "_ga": "GA1.2.510722999.1585849893"
}
response = requests.get('https://csgo500.com/crash/history/before/', cookies=cookie)
JsonHistory = json.loads(response.text)
k = 1
####### cookie
response = requests.get('https://csgo500.com/crash/history/before/', cookies=cookie)
JsonHistory = json.loads(response.text)
k = 1

for element in JsonHistory:
    KeysOfPlays.append(element["roundId"])
    Data = element["endDate"]
    # нужна проверка наличия  в базе (также подключить mysql ,  к примеру. чтобы вести записи, но пока просто на вывод).
    Link = 'https://csgo500.com/crash/history/single/' + str(element["roundId"])
    ResponseBet = requests.get(Link, cookies=cookie)
    JsonBets = json.loads(ResponseBet.text)

    #Если посмотреть данные ссылки типа
    # 'https://csgo500.com/crash/history/single/' + str(element["roundId"])
    # можно заметить, что внутри json имеется некий массив "bets". Однако в python он не виден.


    for BetTime in JsonBets:
        RoundID = BetTime['roundId']
        CrashValue = BetTime['crashValue']
        Bets = BetTime['bets']

        for Bet in Bets:
             SumBet = SumBet + Bet['profit']

    SumBets = SumBets + SumBet
    if k < 2:
        datefirst = Data
    k = k + 1

#datefirst
#SumBets

### Парсер
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Пойдешь в боулинг?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == '😊 Пойдешь в боулинг?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Да, конечно", callback_data='good')
            item2 = types.InlineKeyboardButton("Сори, нет", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Пойдешь в боулинг?",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)

