#!/usr/bin/python
'''
Created on 11.09.2011

@author: corwin
'''

import json
import re

from errors import *
from db_connect import * 
from db_connect import db as dbi 
import sqlalchemy

import config
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
		if config.DEBUG:
			print (request);
		if not isinstance(request, dict):
			raise BadJson("Json must be is object")
		try:
			if "action" not in request.keys():
				raise BadAction("Not Comand")

			res = actions[request.pop("action")](**request)
			if config.DEBUG:
				print("res = {0}".format(res))
			return res
		except (KeyError):
			if config.DEBUG:
				if "getMessages" not in actions.keys():
					print ("cat'n find getMessages")
			raise BadAction()
		except (TypeError):
			if config.DEBUG:
				print ("cat'n find all params ")
			raise BadAction()
	except ValueError:
		raise BadJson('Error in JSON syntax') 

def responded_ok(AdditionParams = None):
	res = {"result":"ok"}
	if AdditionParams != None:
		res.update(AdditionParams)
	return res	
		
def check_username(name):
	if config.DEBUG:
		print("name {0}".format(name))
	if not re.match(config.usrnameRegexp, name, re.I):
		raise BadUsername()

def check_password(pas):
	if not re.match(config.pasRegexp, pas, re.I):
		raise BadPassword() 

def reset_server():
	if DEBUG:
		dbi.clear()
	return {"result":"ok"}

def register_user(username, password):
	check_username(username)
	check_password(password)
	
	if config.DEBUG:
			print("sid before {0}".format(dbi.lastSid))
	
	if dbi.query(User).filter_by(name = username).count() != 0:
		raise UsernameTaken()
	newUser = User(username, password)
	dbi.add(newUser)
	return responded_ok()

def login_user(username,password):
	check_username(username)
	check_password(password)
		 
	try: #потом могет из дб кидать
		user = dbi.query(User).filter_by(name = username).one()
		if user.password != password: 
			raise BadUsernameOrPassword()
		
		user.setSid()
		user.setUserId()
		return responded_ok({"sid": user.sid, "userId":user.userId})
	except sqlalchemy.orm.exc.NoResultFound:
		raise BadUsernameOrPassword()

def logout_user(sid):
	try:
		user = dbi.query(User).filter_by(sid = sid).one() 
		user.sid = None
		dbi.commit()
		return responded_ok()
	except sqlalchemy.orm.exc.NoResultFound:
		raise BadUserSid()

def send_message(sid, text):
	user = dbi.getUser(sid)
	dbi.add(Chat(sid, text));
	return	responded_ok();

def get_messages(since, count = 100):
	return responded_ok(
		{'messages': [{'id': rec.id , 'text': rec.message, 'time': rec.time, 'username': rec.senderUser.name} 
			for rec in dbi.getMessages(since, count)]
		})
		
def upload_map(mapName, playersNum, turnsNum, thumbnail=None, picture=None, regions =None ):
	
	newMap = Map(mapName, playersNum, turnsNum, thumbnail, picture)
	dbi.add(newMap)
	return responded_ok({"mapId":newMap.id})

def get_maps_list():
	try:
		return responded_ok({"mapList": [map[0] for map in dbi.query(Map.id).all()]})
	except:
		raise NotMaps() 

def create_def_maps():
	for newMap in config.DEFAULT_MAPS:
		upload_map(**newMap)
	return responded_ok()

def create_game(sid, gameName, mapId, gameDescription=None):
	dbi.checkSid(sid)
	
	newGame = Game(gameName, mapId, gameDescription)
	dbi.add(newGame)
	
	try:
		join_game(sid, newGame.id)
	except (RequestException):
		dbi.rm(newGame)
		raise AlreadyInGame()  
	return responded_ok({"gameId":newGame.id})

def join_game(sid, gameId):
	dbi.getUser(sid).joinGame(gameId)
	return responded_ok()

def leave_game(sid):
	dbi.getUser(sid).leaveGame()
	return responded_ok()

def get_games_list():
	try:
		return responded_ok({"gamesList": [game[0] for game in dbi.query(Game.id).all()]})
	except:
		raise NotGames() 
	
actions = {
				"register": register_user,
				"login": login_user,
				"logout": logout_user,
				"uploadMap": upload_map,
				"getMapsList": get_maps_list,
				"createDefaultMaps": create_def_maps,
				"createGame":create_game,
				"getGamesList": get_games_list,
				"joinGame": join_game,
				"leaveGame": leave_game,
				"sendMessage": send_message,
				"getMessages" : get_messages,
				"resetServer": reset_server,
}
