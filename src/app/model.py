import json
import peewee
from enum import Enum
from playhouse.shortcuts import dict_to_model, model_to_dict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pprint import pprint

if __name__ == '__main__':
    from config import Config
else:
    from app.config import Config


db = peewee.SqliteDatabase(Config.SQLITE3_DATABASE_PATH)


class UserLogType(Enum):
    LOGIN = 0
    LOGOUT = 1


class QueryType(Enum):
    REGION = 0
    CATEGORY = 1


class ProductRegion(peewee.Model):
    id       = peewee.IntegerField(primary_key=True)
    name     = peewee.CharField()

    class Meta:
        database = db
        table_name = 'product_region'


class ProductCategory(peewee.Model):
    id       = peewee.IntegerField(primary_key=True)
    name     = peewee.CharField()

    class Meta:
        database = db
        table_name = 'product_category'


class Product(peewee.Model):
    id          = peewee.IntegerField(primary_key=True)
    region_id   = peewee.IntegerField()
    category_id = peewee.IntegerField()
    name        = peewee.CharField()
    price       = peewee.CharField()
    sales       = peewee.IntegerField()
    description = peewee.TextField()

    class Meta:
        database = db


class ProductImage(peewee.Model):
    id         = peewee.IntegerField(primary_key=True)
    product_id = peewee.IntegerField()
    filename   = peewee.CharField()

    class Meta:
        database = db
        table_name = 'product_image'


class User(peewee.Model):
    id       = peewee.IntegerField(primary_key=True)
    age      = peewee.IntegerField()
    address  = peewee.CharField()

    class Meta:
        database = db


class UserLog(peewee.Model):
    id          = peewee.IntegerField(primary_key=True)
    type        = peewee.IntegerField()
    user_id     = peewee.IntegerField()
    create_time = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'user_log'


class QueryLog(peewee.Model):
    id          = peewee.IntegerField(primary_key=True)
    user_id     = peewee.IntegerField()
    query_type  = peewee.IntegerField()
    query_id    = peewee.IntegerField()
    create_time = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'query_log'


class DetailLog(peewee.Model):
    id          = peewee.IntegerField(primary_key=True)
    user_id     = peewee.IntegerField()
    product_id  = peewee.IntegerField()
    create_time = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'detail_log'


class PurchaseLog(peewee.Model):
    id          = peewee.IntegerField(primary_key=True)
    user_id     = peewee.IntegerField()
    product_id  = peewee.IntegerField()
    create_time = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'purchase_log'


if __name__ == '__main__':
    MODELS = [ProductRegion, ProductCategory, Product, ProductImage, User, UserLog, QueryLog, DetailLog, PurchaseLog]
    db.drop_tables(MODELS)
    db.create_tables(MODELS)

    product_regions = json.load(open('db/init/product_region.json'))
    product_categories = json.load(open('db/init/product_category.json'))
    products = json.load(open('db/init/product.json'))
    product_images = json.load(open('db/init/product_image.json'))

    ProductRegion.insert_many(product_regions).execute()
    ProductCategory.insert_many(product_categories).execute()
    Product.insert_many(products).execute()
    ProductImage.insert_many(product_images).execute()
