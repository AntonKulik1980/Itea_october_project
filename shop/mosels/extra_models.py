from .shop_models import Time_stamp
from . import me



class News(Time_stamp):
    title = me.StringField(required=True,min_length=2,max_length=256)
    body = me.StringField(required=True,min_length=2,max_length=2048)
    # TODO datetime class