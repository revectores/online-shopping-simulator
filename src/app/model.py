if __name__ == '__main__':
    import sys
    sys.path.append('..')

import json
import codecs

from enum import Enum
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import peewee
from playhouse.shortcuts import dict_to_model, model_to_dict

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


class QueryBackLog(peewee.Model):
    id          = peewee.IntegerField(primary_key=True)
    user_id     = peewee.IntegerField()
    query_type  = peewee.IntegerField()
    query_id    = peewee.IntegerField()
    create_time = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'query_back_log'


class DetailBackLog(peewee.Model):
    id          = peewee.IntegerField(primary_key=True)
    user_id     = peewee.IntegerField()
    product_id  = peewee.IntegerField()
    create_time = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'detail_back_log'


class PurchaseLog(peewee.Model):
    id          = peewee.IntegerField(primary_key=True)
    user_id     = peewee.IntegerField()
    product_id  = peewee.IntegerField()
    create_time = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'purchase_log'


def db_init():
    def load_init_data(table_name):
        return json.load(codecs.open(f'{Config.ROOT}/db/init/{table_name}.json', encoding='utf-8'))

    MODELS = [ProductRegion, ProductCategory, Product, ProductImage, User, UserLog, QueryLog, DetailLog, PurchaseLog, QueryBackLog, DetailBackLog]
    db.drop_tables(MODELS)
    db.create_tables(MODELS)

    product_regions = load_init_data('product_region')
    product_categories = load_init_data('product_category')
    products = load_init_data('product')
    product_images = load_init_data('product_image')

    ProductRegion.insert_many(product_regions).execute()
    ProductCategory.insert_many(product_categories).execute()
    Product.insert_many(products).execute()
    ProductImage.insert_many(product_images).execute()


if __name__ == '__main__':
    db_init()
