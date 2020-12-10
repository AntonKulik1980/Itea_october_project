from telebot import TeleBot
from.config import TOKEN
from .constants import GREETINGS
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    name= getattr(message.from_user,'first_name')
    greetings = GREETINGS.format(message.from_user.first_name)
    bot.send.message(message.chat.id, greetings)

