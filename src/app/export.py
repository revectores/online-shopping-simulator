if __name__ == '__main__':
    import sys
    sys.path.append('..')

import csv
import operator

from pprint import pprint

from app.config import Config
from app.model import UserLogType, QueryType
from app.model import ProductRegion, ProductCategory, Product, User
from app.model import UserLog, QueryLog, DetailLog, PurchaseLog

from app.utils import models_to_dict


def export(user_id=0):
    EXPORT_ALL = (user_id == 0)
    mode = 'w' if EXPORT_ALL else 'a'

    with open(Config.EXPORT_PATH / 'user.csv', mode, newline='') as user_csv:
        user_query = User.select()
        if not EXPORT_ALL:
            user_query = user_query.where(User.id == user_id)

        users = [[user.id,
                  user.age,
                  user.address] for user in user_query]

        writer = csv.writer(user_csv)
        
        if user_csv.tell() == 0:
            writer.writerow(['id', 'age', 'address'])

        writer.writerows(users)


    with open(Config.EXPORT_PATH / 'activity.csv', mode, newline='') as activity_csv:
        product_regions    = {region.id: region.name for region in ProductRegion.select()}
        product_categories = {category.id: category.name for category in ProductCategory.select()}
        products           = {product.id: product.name for product in Product.select()}

        user_log_query     = UserLog.select()
        query_log_query    = QueryLog.select()
        detail_log_query   = DetailLog.select()
        purchase_log_query = PurchaseLog.select()

        if not EXPORT_ALL:
            user_log_query = user_log_query.where(UserLog.user_id == user_id)
            query_log_query = query_log_query.where(QueryLog.user_id == user_id)
            detail_log_query = detail_log_query.where(DetailLog.user_id == user_id)
            purchase_log_query = purchase_log_query.where(PurchaseLog.user_id == user_id)

        user_logs = [[
            'log in' if user_log.type == UserLogType.LOGIN.value else 'log out',
            user_log.user_id,
            '',
            user_log.create_time
        ] for user_log in user_log_query]

        query_logs = [[
            'region' if query_log.query_type == QueryType.REGION.value else 'category',
            query_log.user_id,
            product_regions[query_log.query_id] if query_log.query_type == QueryType.REGION.value else product_categories[query_log.query_id],
            query_log.create_time
        ] for query_log in query_log_query]

        detail_logs = [[
            'detail',
            detail_log.user_id,
            products[detail_log.product_id],
            detail_log.create_time
        ] for detail_log in detail_log_query]
        
        purchase_logs = [[
            'purchase',
            purchase_log.user_id,
            products[purchase_log.product_id],
            purchase_log.create_time
        ] for purchase_log in purchase_log_query]

        writer = csv.writer(activity_csv)

        if activity_csv.tell() == 0:
            writer.writerow(['type', 'user_id', 'object', 'datetime'])

        logs = user_logs + query_logs + detail_logs + purchase_logs
        logs.sort(key=operator.itemgetter(3))
        writer.writerows(logs)


if __name__ == '__main__':
    export(0)
