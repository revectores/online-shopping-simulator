from flask import jsonify


def suc(data={}):
	return jsonify({'code': 0, 'msg': '', 'data': data})

def err(msg='', code=1, data={}):
	return jsonify({'code': code, 'msg': msg, 'data': data})
