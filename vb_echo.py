import telebot
from telebot.types import Message, User
import hparse
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    usr: User = message.from_user
    bot.send_message(chat_id=message.chat.id, text='Hello, {}! It\'s very nice to meet you!'.format(usr.first_name))


@bot.message_handler(commands=['habr'])
def send_welcome(message: Message):
    text_message = hparse.get_links(hub_name='Python', path=hparse.__file__)
    if len(text_message) == 0:
        text_message = 'There is no new interesting articles.'
    bot.send_message(chat_id=message.chat.id, text=text_message)


@bot.message_handler(func=lambda m: True)
def echo_all(message: Message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True, interval=0, timeout=200)
