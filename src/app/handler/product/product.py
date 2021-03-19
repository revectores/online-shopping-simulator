from datetime import datetime, timedelta

from flask import Blueprint, send_from_directory, jsonify, request, session, redirect, url_for
from playhouse.shortcuts import dict_to_model, model_to_dict

from app.model import QueryType
from app.model import Product, ProductRegion, ProductCategory, ProductImage
from app.model import QueryLog, DetailLog, PurchaseLog, QueryBackLog, DetailBackLog
from app.utils import models_to_dict
from app.resp import suc, err


product = Blueprint('product', __name__)
product_api = Blueprint('product_api', __name__)


@product.route('/list/')
def html_product_list():
    if 'user_id' not in session:
        return redirect(url_for('user.html_login'))

    return send_from_directory('templates/product/', 'list.html')


@product.route('/<int:product_id>')
def html_product_detail(product_id):
    if 'user_id' not in session:
        return redirect(url_for('user.html_login'))

    return send_from_directory('templates/product', 'detail.html')


@product_api.route('/product')
def get_product():
    region_id = request.args.get('region_id')
    category_id = request.args.get('category_id')

    assert(region_id or category_id)

    if region_id:
        QueryLog.insert({
            'user_id': session['user_id'],
            'query_type': QueryType.REGION.value,
            'query_id': region_id
        }).execute()
        return suc(models_to_dict(Product.select().where(Product.region_id == region_id)))

    if category_id:
        QueryLog.insert({
            'user_id': session['user_id'],
            'query_type': QueryType.CATEGORY.value,
            'query_id': category_id
        }).execute()
        return suc(models_to_dict(Product.select().where(Product.category_id == category_id)))


@product_api.route('/region')
def get_product_region():
    return suc(models_to_dict(ProductRegion.select()))


@product_api.route('/category')
def get_product_category():
    return suc(models_to_dict(ProductCategory.select()))


@product_api.route('/<int:product_id>')
def product_detail(product_id):
    DetailLog.insert({
        'user_id': session['user_id'],
        'product_id': product_id,
    }).execute()

    return suc(model_to_dict(Product.get(product_id)))


@product_api.route('/image/<int:product_id>')
def get_product_images(product_id):
    return suc([p.filename for p in ProductImage.select().where(ProductImage.product_id == product_id)])


@product_api.route('/repr_image/<int:product_id>')
def get_product_repr_image(product_id):
    return suc(ProductImage.get(ProductImage.product_id == product_id).filename)


@product_api.route('/purchase/<int:product_id>', methods=["POST"])
def purchase(product_id):
    PurchaseLog.insert({
        'user_id':  session['user_id'],
        'product_id': product_id,
    }).execute()
    return suc()


@product_api.route('/back', methods=['POST'])
def back():
    pathname, query = request.json['pathname'], request.json['search'].removeprefix('?')

    if request.json['pathname'] == '/product/list/':
        query_key, query_id = query.split('=')
        QueryBackLog.insert({
            'user_id': session['user_id'],
            'query_type': QueryType.REGION.value if query_key == 'region_id' else QueryType.CATEGORY.value,
            'query_id': query_id
        }).execute()
    else:
        product_id = pathname.split('/')[-1]
        DetailBackLog.insert({
            'user_id': session['user_id'],
            'product_id': product_id
        }).execute()

    return suc()
