from flask import Blueprint, send_from_directory, jsonify


user = Blueprint('user', __name__)
user_api = Blueprint('user_api', __name__)


@user.route('/login')
def html_login():
	return send_from_directory('templates/user/', 'login.html')
