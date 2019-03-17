import pprint
import telebot
from telebot import apihelper
from telebot.types import Message, User

#apihelper.proxy = {'https':'socks5://telegram:telegram@qcpfo.tgproxy.me:1080'}
apihelper.proxy = {'https':'socks5://tg-denvyugo:YpGvFmAi@socksy.seriyps.ru:7777'}
#apihelper.proxy = {'http':'http://10.10.1.10:3128'}
bot = telebot.TeleBot('758896761:AAGhUuuBz9P-p4lFvP5Dsi3wi4ftc8Jt1NQ')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    usr: User = message.from_user
    bot.send_message(chat_id=message.chat.id, text='Hello, {}! It\'s very nice to meet you!'.format(usr.first_name))


@bot.message_handler(func=lambda m: True)
def echo_all(message: Message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True, interval=0, timeout=200)
