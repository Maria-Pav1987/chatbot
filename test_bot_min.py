import requests
import telebot
from telebot import types
import json

bot = telebot.TeleBot('6593300298:AAEWcG4JOQjbnuLRB890fG9JWT-MkioysS0')
API = '19ba22ee457e853446eb51d80bd51773'

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn_good = types.KeyboardButton('Отлично!')
    btn_sad = types.KeyboardButton('Грустненько...')
    markup.row(btn_good, btn_sad)
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}! Как твои дела?', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Отлично!':
        markup = types.InlineKeyboardMarkup()
        btn_news = types.InlineKeyboardButton('Почитаем новости?🤓', callback_data='news', url='https://meduza.io')
        btn_walking = types.InlineKeyboardButton('Погуляем🤠?', callback_data='walking')
        markup.row(btn_news, btn_walking)
        bot.reply_to(message, f'{message.from_user.first_name}! Рада слышать! Тогда что поделаем?', reply_markup=markup)
    elif message.text == 'Грустненько...':
        markup = types.InlineKeyboardMarkup()
        btn_films = types.InlineKeyboardButton('Посмотрим фильмы?👁', callback_data='films', url='https://www.kinopoisk.ru')
        btn_memes = types.InlineKeyboardButton('Полистаем мемасики?👉', callback_data='memes', url='https://www.reddit.com/r/memes/')
        markup.row(btn_films, btn_memes)
        bot.reply_to(message, f'{message.from_user.first_name}! Ну тогда нужно немного FUN!', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'news':
        bot.send_message(callback.message.chat.id, 'Здорово, почитаем новости?')
    elif callback.data == 'walking':
        bot.send_message(callback.message.chat.id, 'Отлично, погуляем? Ты сейчас где?')
    elif callback.data == 'films':
        bot.send_message(callback.message.chat.id, 'Жаль слышать, отвлечемся на фильмы?')
    elif callback.data == 'memes':
        bot.send_message(callback.message.chat.id, 'Тогда, может, полистаем мемасики?')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = json.loads(res.text)
    temp = data["main"]["temp"]
    if temp > 5.0:
        bot.reply_to(message, f'Сейчас погода {temp} градусов. Скорость ветра {data["wind"]["speed"]} метр/сек. Иди гулять 😎')
    else:
        bot.reply_to(message, f'Сейчас погода {temp} градусов. Скорость ветра {data["wind"]["speed"]} метр/сек. Пожалуй, лучше посидеть дома 🥶, можно почитать новости!')

bot.polling(none_stop=True)
