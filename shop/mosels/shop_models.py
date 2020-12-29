import mongoengine as me
import datetime
me.connect('SHOP')

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
    first_name = me.StringField(min_length=2,max_length=128)
    phone_number = me.StringField(max_length=12)
    adress = me.StringField(max_length=20)
    email = me.EmailField()
    is_blocked = me.BooleanField(default=False)

    @classmethod
    def get_updateble_settings(cls):
        return cls.first_name

    def formatted_data(self):
        return f'id- {self.telegram_id}\nНикнейм- {self.username}\n,name-{self.first_name}\n, ' \
               f'email-{self.email}\nPhone- {self.phone_number}'

    def get_active_cart(self):
        cart = Cart.objects(user=self,is_active=True).first()
        if not cart:
            cart = Cart.objects.create(
                user=self)
            return cart
        return cart



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
    def get_products(self):
        return Product.objects(category=self)


class Param(me.EmbeddedDocument):
    height = me.FloatField()
    width = me.FloatField()
    weight = me.FloatField()
    additional_description = me.StringField()


class Product(Time_stamp):
    title = me.StringField(required=True,max_length=256)
    description = me.StringField(min_length=512)
    in_stock = me.BooleanField(default=True)
    discount = me.IntField(min_value=0,max_value=100)
    price = me.FloatField(required=True)
    image = me.FileField()
    category = me.ReferenceField(Category,required=True)
    parameters = me.EmbeddedDocumentField(Param)

    @property
    def product_price(self):
        (100-self.discount)/100 * self.price


    def formatted_product(self):
        return f'Цена-{self.price}\nНазвание-{self.title}\nОписание-' \
               f'{self.description}\nхарактеристики:{self.parameters}'




class News(Time_stamp):
    title = me.StringField(required=True,min_length=2,max_length=256)
    body = me.StringField(required=True,min_length=2,max_length=2048)
    def get_news(self):
        return News.objects()


class Cart(Time_stamp):
    user = me.ReferenceField(User, required=True)
    products = me.ListField(me.ReferenceField(Product))
    is_active =me.BooleanField(default=True)

    def add_product(self,product):
        self.products.append(
            product )
        self.save()




class Order(Time_stamp):
    User = me.ReferenceField(User,required=True)
    Products = me.ListField(me.ReferenceField(Cart))



# User(telegram_id='678678',username ='Petr',phone_number ='5787878',).save()
#
# User(telegram_id='243523',username ='IVAN',phone_number ='374633').save()
# Создать абстрактную коллекцию. Она должна содержать поля креатед и модифайд и хранить в них дату и время.
# Логику со временем разместить в методе save.


