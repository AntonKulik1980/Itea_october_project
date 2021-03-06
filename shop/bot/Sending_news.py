from ..bot.shop_bot import bot
# from ..mosels.shop_models import User
from shop.mosels.shop_models import User
from telebot.apihelper import ApiException
from threading import Thread

import time


class Sender:

    def __init__(self, users, **message_data):
        self._message_data = message_data
        self._users = users

    def send_message(self):
        users = self._users.filter(is_blocked=False)
        blocked_ids = []
        for u in users:
            try:
                bot.send_message(
                    u.telegram_id,
                    **self._message_data
                )
            except ApiException as e:
                if e.error_code == 403:
                    blocked_ids.append(u.telegram_id)
                else:
                    raise e
            time.sleep(0.1)

        User.objects(telegram_id_in=blocked_ids).update(is_blocked=True)



def cron_unlock_users():
    while True:
        User.objects(is_blocked=True).update(is_blocked=False)
        minute = 60
        hour = 60*minute
        day= 24*hour
        time.sleep(2*day)

Thread(target=cron_unlock_users).start()






