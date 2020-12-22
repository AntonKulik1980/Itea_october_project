from shop.bot.Sending_news import Sender
from shop.mosels.shop_models import User
from telebot.types import ReplyKeyboardMarkup,KeyboardButton

kb = ReplyKeyboardMarkup(resize_keyboard=True)
discount = KeyboardButton(text='New button')
kb.add(discount)
s=Sender(User.objects(),reply_markup=kb,text='Attention! new button')
s.send_message()
