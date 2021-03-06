from flask import Blueprint, send_from_directory, jsonify, request
from playhouse.shortcuts import dict_to_model, model_to_dict

from app.model import Product, ProductRegion, ProductCategory, ProductImage
from app.utils import models_to_dict
from app.resp import suc, err


product = Blueprint('product', __name__)
product_api = Blueprint('product_api', __name__)


@product.route('/list/')
def html_product_list():
    return send_from_directory('templates/product/', 'list.html')


@product.route('/<int:product_id>')
def html_product_detail(product_id):
    return send_from_directory('templates/product', 'detail.html')


@product_api.route('/product')
def get_product():
    region_id = request.args.get('region_id')
    category_id = request.args.get('category_id')

    assert(region_id or category_id)

    if region_id:
        return suc(models_to_dict(Product.select().where(Product.region_id == region_id)))

    if category_id:
        return suc(models_to_dict(Product.select().where(Product.category_id == category_id)))


@product_api.route('/region')
def get_product_region():
    return suc(models_to_dict(ProductRegion.select()))


@product_api.route('/category')
def get_product_category():
    return suc(models_to_dict(ProductCategory.select()))


@product_api.route('/<int:product_id>')
def product_detail(product_id):
    return suc(model_to_dict(Product.get(product_id)))


@product_api.route('/image/<int:product_id>')
def get_product_images(product_id):
    return suc([p.filename for p in ProductImage.select().where(ProductImage.product_id == product_id)])


@product_api.route('/repr_image/<int:product_id>')
def get_product_repr_image(product_id):
    return suc(ProductImage.get(ProductImage.product_id == product_id).filename)
