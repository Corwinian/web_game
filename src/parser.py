#!/usr/bin/python
'''
Created on 11.09.2011

@author: corwin
'''

import json
from errors import *
from db_connect import * 
from db_connect import db as dbi 
import sqlalchemy
from config import JSON_DUMPS_FORMAT

actions = {}

def parse_request(request): #думал написать комплить но не уверен в верности фразы 
	json_dump = lambda dict: json.dumps(dict, **JSON_DUMPS_FORMAT)
	try:
		return json_dump(do_request(request))
	except (RequestException) as e:
		return json_dump(e.toDict())

def do_request(request):
	try:
		request = (json.loads(request))
		if not isinstance(request, dict):
			raise BadJson("Json must be is object")
		try:
			if "action" not in request.keys():
				raise BadAction("Not Comand")
			return actions[request.pop("action")](**request)
		except (KeyError):
			raise BadAction("Unindefined command")
	except ValueError:
		raise BadJson('Error in JSON syntax') 
		
def check_username(name):
	return True

def check_password(pas):
	return True

def register_user(username, password):
	if not check_username(username):
		raise BadUserName(); 
	if not check_password(password):
		raise BadPassword(); 
	if dbi.query(User).filter_by(name="user").count() != 0:
		raise UsernameTaken()
	dbi.add(User(username, password))
	return responded_ok()

def login_user(userame):
	if not check_username(username):
		raise BadUserName(); 
	if not check_password(password):
		raise BadPassword(); 
	try: #потом могет из дб кидать
		userInDb = dbi.query(User).filter_by(name = user.name).one()
		if userInDb.password != password: 
			raise BadNameOrPassword()
		user = User(user, password)
		return responded_ok({"sid": user.create_sid()})
	except sqlalchemy.orm.exc.NoResultFound:
		raise BadNameOrPassword("Wrong username")
	return

def logout_user(sid):
	try:
		user =data_Base.query(User).filter_by(sid = sid).one() 
		user.sid=None
		data_Base.commit()
		return responded_ok()
	except sqlalchemy.orm.exc.NoResultFound:
		raise NotUser("UserUnRegiser")
	

def responded_ok(AdditionParams = None):
	res = {"status":"ok"}
	if AdditionParams != None:
		for param in AdditionParams:
			res.add(param)
	return res


actions = {
				"register": register_user,
				"login": "login_user",
				"logout": "logout_user",
}
