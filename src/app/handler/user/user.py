from datetime import datetime, timedelta

from flask import Blueprint, send_from_directory, jsonify, request, session, redirect, url_for
from playhouse.shortcuts import dict_to_model, model_to_dict

from app.model import User, UserLog, UserLogType
from app.resp import suc, err
from app.export import export


user = Blueprint('user', __name__)
user_api = Blueprint('user_api', __name__)


@user.route('/login')
def html_login():
	return send_from_directory('templates/user/', 'login.html')


@user_api.route('/login', methods=['POST'])
def api_login():
	user_id = User.get_or_none(request.json['id'])
	if user_id:
		return err('该序号已被使用')

	new_user_id = User.insert(request.json).execute()
	UserLog.insert({
		'type':     UserLogType.LOGIN.value,
		'user_id':  new_user_id,
	}).execute()

	session['user_id'] = new_user_id
	return suc()


@user_api.route('/logout', methods=['POST'])
def api_logout():
	if 'user_id' not in session:
		return suc()

	user_id = session['user_id']

	UserLog.insert({
		'type': UserLogType.LOGOUT.value,
		'user_id': user_id
	}).execute()

	session.pop('user_id', None)

	export(user_id)
	return suc()
