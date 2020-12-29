from shop.bot.shop_bot import bot, app
import time
from shop.bot.config import TOKEN,WEBHOOK_URI,WEBHOOK_URL
#bot.polling()

bot.remove_webhook()
time.sleep(0.5)
bot.set_webhook(WEBHOOK_URL, certificate=open('webhook_cert.pem'))
app.run(debug=True)