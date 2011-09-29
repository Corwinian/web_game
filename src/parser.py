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
		raise BadJson('Error in JSON syntaxa') 
		
def check_username(name):
	return True

def check_password(pas):
	return True

def register_user(username, password):
	if not check_username(username):
		raise BadUserName(); 
	if not check_password(password):
		raise BadPassword(); 
	if dbi.query(User).filter_by(name = username).count() != 0:
		raise UsernameTaken()
	newUser = User(username, password)
	dbi.add(newUser)
	return responded_ok()

def login_user(username,password):
	if not check_username(username):
		raise BadUserName(); 
	if not check_password(password):
		raise BadPassword(); 
	try: #потом могет из дб кидать
		user = dbi.query(User).filter_by(name = username).one()
		if user.password != password: 
			raise BadUsernameOrPassword()
		user.setSid()
		return responded_ok({"sid": user.sid})
	except sqlalchemy.orm.exc.NoResultFound:
		raise BadUsernameOrPassword("Wrong username")


def logout_user(sid):
	try:
		user = dbi.query(User).filter_by(sid = sid).one() 
		user.sid = None
		dbi.commit()
		return responded_ok()
	except sqlalchemy.orm.exc.NoResultFound:
		raise BadSid()

def upload_map(mapName, playersNum):
	if 1 > len(mapName) > 15 or not mapName.isprintable():
		raise BadMapName()
	if 1 > playersNum > 5: 
		raise BadPlayersNum()
	newMap  = Map(mapName, playersNum)
	dbi.add(newMap)
	return responded_ok({"mapId":newMap.id})

def get_maps_list():
	try:
		return responded_ok({"mapList": [map[0] for map in dbi.query(Map.id).all()]})
	except:
		raise NotMaps() 

def create_def_maps ():
	for i in range(1, 4):
		dbi.add(Map("defaultMap" + str(i) , i + 1))
	return responded_ok()

def create_game(sid, gameName, mapId, gameDescr=None):
	if not dbi.checkSid(sid):
		raise BadSid()

	newGame = Game(gameName, mapId, gameDescr)
	dbi.add(newGame)
	return responded_ok({"gameId":newGame.id})

def join_game(sid, gameId):
	dbi.gameUser(sid).joinGame(gameId)
	return responded_ok()

def leave_game(sid):
	dbi.gameUser(sid).leaveGame()
	return responded_ok()

def get_games_list():
	try:
		return responded_ok({"gamesList": [game[0] for game in dbi.query(Game.id).all()]})
	except:
		raise NotGames() 

def responded_ok(AdditionParams = None):
	res = {"status":"ok"}
	if AdditionParams != None:
		res.update(AdditionParams)
	return res

actions = {
				"register": register_user,
				"login": login_user,
				"logout": logout_user,
				"uploadMap": upload_map,
				"getMapsList": get_maps_list,
				"createGame":create_game,
				"getGamesList": get_games_list,
				"joinGame": join_game,
				"leaveGame": leave_game,
}
