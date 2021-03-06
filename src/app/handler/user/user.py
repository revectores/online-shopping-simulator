from datetime import datetime, timedelta

from flask import Blueprint, send_from_directory, jsonify, request
from playhouse.shortcuts import dict_to_model, model_to_dict

from app.model import User, UserLog, UserLogType
from app.resp import suc, err


user = Blueprint('user', __name__)
user_api = Blueprint('user_api', __name__)


@user.route('/login')
def html_login():
	return send_from_directory('templates/user/', 'login.html')


@user_api.route('/login', methods=["POST"])
def login():
	user_id = User.get_or_none(request.json['id'])
	if user_id:
		return err('该序号已被使用')

	new_user_id = User.insert(request.json).execute()
	UserLog.insert({
		'type':     UserLogType.LOGIN.value,
		'user_id':  new_user_id,
	}).execute()

	return suc()
