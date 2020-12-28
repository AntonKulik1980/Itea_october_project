import json
from flask import Flask,request,abort
from telebot.types import Update
import time
from mongoengine import NotUniqueError
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup,KeyboardButton,Message
from shop.mosels.shop_models import Category
from shop.mosels.shop_models import News
from shop.mosels.shop_models import User
from shop.mosels.shop_models import Product
from shop.bot.config import TOKEN,WEBHOOK_URI,WEBHOOK_URL
from shop.bot import constants
from shop.bot.utils import inline_kb_from_iterable
bot = TeleBot(TOKEN)

app = Flask(__name__)


@bot.message_handler(commands=['start'])
def handle_start(message):
    name = f', {message.from_user.first_name}' if getattr(message.from_user, 'first_name') else ''
    greetings = constants.GREETINGS.format(name)
    try:
        User.objects.create(
        telegram_id=message.chat.id,
        username= getattr(message.from_user,'username',None),
        first_name=getattr(message.from_user, 'first_name',None)
        )
    except NotUniqueError:
        greetings = f'Welcome back'
    else:
        name = f', {message.from_user.first_name}' if getattr(message.from_user, 'first_name') else ''
        greetings = constants.GREETINGS.format(name)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [InlineKeyboardButton(n) for n in constants.START_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, greetings,reply_markup=kb)



@bot.message_handler(func=lambda m: constants.START_KB[constants.CATEGORIES] == m.text)
def handle_categories(message:Message):
    kb= InlineKeyboardMarkup()
    root_categories = Category.get_root_categories()
    kb = inline_kb_from_iterable(constants.CATEGORY_TAG,root_categories)
    bot.send_message(
        message.chat.id,
        'Выберите категорию!',
        reply_markup=kb
    )

@bot.message_handler(func=lambda m: constants.START_KB[constants.NEWS] == m.text)
def handle_news(message):
    news = News.get_news()
    for n in news:

        bot.send_message(
            message.chat.id,
            n.body
        )





@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.CATEGORY_TAG)
def handle_category(call):
    category = Category.objects.get(id=json.loads(call.data)['id'])

    if category.subcategories:
        kb= inline_kb_from_iterable(constants.CATEGORY_TAG,category.subcategories)
        bot.edit_message_text(
            category.title,
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=kb
        )
        bot.send_message(call.message.chat.id,category.title,reply_markup=kb)
    else:
        products= category.get_products()
        for p in products:
            kb= InlineKeyboardMarkup()
            button = InlineKeyboardButton(
                text=constants.ADD_TO_CARD,
                callback_data=json.dumps({
                    'id': str(p.id),
                    'tag':constants.PRODUCT_TAG
                }
                    )

                    )
            kb.add(button)
            #description = p.description if p.description else ''
            bot.send_photo(
                call.message.chat.id,
                p.image.read(),
                caption = p.formatted_product(),
                reply_markup=kb
            )




@bot.message_handler(func=lambda m: constants.START_KB[constants.SETTINGS] == m.text)
def handle_settings(message):
    user = User.objects.get(telegram_id=message.chat.id)
    data = user.formatted_data()
    settings= User.get_updateble_settings()
    kb = InlineKeyboardMarkup()
    kb = inline_kb_from_iterable(constants.SETTINGS_TAG,settings)
    bot.send_message(
        user.telegram_id,
       data,
       reply_markup=kb)








@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == constants.PRODUCT_TAG)
def handle_product_add_to_cart(call):
    producct_id = json.loads(call.data)['id']
    product = Product.objects.get(id=producct_id)
    user = User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_active_cart()
    cart.add_product(product)
    bot.answer_callback_query(
        call.id,
        'Продукт добавлен в корзину'
    )



@app.route(WEBHOOK_URI, methods=['POST'])
def handle_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    abort(403)

















