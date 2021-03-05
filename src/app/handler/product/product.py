from flask import Blueprint, send_from_directory, jsonify, request


product = Blueprint('product', __name__)
product_api = Blueprint('product_api', __name__)


@product.route('/product_list/')
def html_product_list():
	request.args.get('region')
	request.args.get('name')

	return send_from_directory('templates/product/', 'product_list.html')


@product.route('/product_detail')
def html_product_detail():
	return send_from_directory('templates/product', 'product_detail.html')
