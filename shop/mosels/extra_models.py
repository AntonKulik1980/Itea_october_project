# from .shop_models import Time_stamp
# from .import me
# import json
# from pymongo import MongoClient
# import mongoengine as me
# import datetime
#
#
#
# class News(me.Document):
#     title = me.StringField(required=True,min_length=2,max_length=256)
#     body = me.StringField(required=True,min_length=2,max_length=2048)
#     # def get_news(self):
#     #     return News.objects()
#
# me.connect('SHOP')
#
# client = MongoClient('localhost', 27017)
# db = client['SHOP']
# collection_currency = db['news']
#
# with open('news.json') as f:
#     file_data = json.load(f)
#
# collection_currency.News.insert_many(file_data)
# client.close()
#



