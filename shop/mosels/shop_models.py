from . import me
import datetime


class Time_stamp(me.Document):
    meta = {
        'abstract': True
    }
    created_at = me.DateTimeField(default=datetime.datetime.now())
    modified_at = me.DateTimeField()
    def save(self,*args,**kwargs):
        self.modified_at = datetime.datetime.now()
        super().save(*args,**kwargs)
    # def update(self,*args,**kwargs):
    #     self.modified_at = datetime.datetime.now()
    #     super().save(*args, **kwargs)

class User(Time_stamp):
    telegram_id = me.IntField(primary_key=True)
    username = me.StringField(min_length=2,max_length=28)
    phone_number = me.StringField(max_length=12)
    email = me.EmailField()
    is_blocked = me.BooleanField(default=False)

class Category(Time_stamp):
    title = me.StringField(required=True)
    description = me.StringField(min_length=512)
    parent =  me.ReferenceField('self')
    subcategories = me.ListField(me.ReferenceField('self'))


    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent =None)


    def is_root(self):
        return not bool(self.parent)


    def add_subcategory(self,category):
        category.parent = self
        category.save()
        self.subcategories.append(category)
        self.save()



class Product(Time_stamp):
    title = me.StringField(required=True,max_length=256)
    description = me.StringField(min_length=512)
    in_stock = me.BooleanField(default=True)
    discount = me.IntField(min_value=0,max_value=100)
    price = me.FloatField(required=True)
    image = me.FileField()
    category = me.ReferenceField(Category,required=True)




# User(telegram_id='243523',username ='IVAN',phone_number ='374633',).save()
#
User(telegram_id='243523',username ='IVAN',phone_number ='374633').save()
# Создать абстрактную коллекцию. Она должна содержать поля креатед и модифайд и хранить в них дату и время.
# Логику со временем разместить в методе save.


