'''
Created on 13.09.2011

@author: corwin
'''
import os

import time

from sqlalchemy import create_engine, Table, Boolean, Enum, Column, Integer, String, MetaData, Date, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, exc, relationship
from sqlalchemy.ext.declarative import declarative_base

from errors import *
from config import DB_CONFIG
from config import DEBUG

import hashlib
import datetime

Base = declarative_base()

pkey = lambda: Column(Integer, primary_key=True)
fkey = lambda name: Column(Integer, ForeignKey(name, onupdate='CASCADE', ondelete='CASCADE'))
string = lambda mayNull=False: Column(String, nullable=mayNull)
integer = lambda mayNull=False: Column(Integer, nullable=mayNull)
bool = lambda isTrue=False: Column(Boolean, default=isTrue)
uniqstring = lambda mayNull=False: Column(String, unique=True, nullable=mayNull)
utcDT = lambda: Column(DateTime, default=utcnow)

class User(Base):
	__tablename__ = "users"
	
	id = pkey()
	name = uniqstring()
	password = string()
	sid = integer(True) if DEBUG else string(True)
	userId = integer(True) if DEBUG else string(True)
	gameId = fkey('games.id')
	isReady = bool()

	def __init__(self, name, password):
		super().__init__()
		self.name = name;
		self.password = password;
	
	def setSid(self):
		if DEBUG:
			self.sid = db.lastSid +1
			db.lastSid = db.lastSid +1
		else:
			seq = str(datetime.datetime.utcnow()) + self.name + self.password
			self.sid = hashlib.sha1(seq.encode("utf-8")).hexdigest()
		db.commit()
	
	def setUserId(self):
		self.userId =  self.sid if self.userId == None else self.userId
		db.commit()
	
	def joinGame(self, gameId):
		if self.gameId is not None:
			raise AlreadyInGame()

		db.getGame(gameId).addPlayer()
		
		self.gameId = gameId
		db.commit()

	def leaveGame(self):
		if self.gameId is None:
			raise NotInGame()

		db.getGame(self.gameId).rmPlayer()
		
		self.gameId = None
		db.commit()

	def setStatus(self, status):
		if self.gameId is None:
			raise NotInGame()
		if db.getGame(self.gameId).gameStatus != Game.gameStatusWaiting: 
			raise BadGameState()
		self.isReady = status
		if status:
			db.getGame(self.gameId).updateStage()

	def __repr__(self):
		return "<User('%s','%s',)>" % (self.name, self.password)

class Map(Base):
	__tablename__ = "maps"
	
	id = pkey()
	name = string()
	playersNumber = integer()
	turnsNum = integer()
	picture = string(True)
	thumbnail = string(True)
	#regions
	
	def __init__(self, name, playersNum, turnsNum, regions=None, picture=None, thumbnail=None):
		super().__init__()
		self.checkMapName(name)
		
		if not  1 < playersNum < 6: 
			raise BadPlayersNum()
				
		if not 4 < turnsNum < 11: 
			raise TurnsNum()
				
		self.name = name
		self.playersNumber = playersNum
		self.turnsNum = turnsNum
		self.picture = picture
		self.thumbnail = thumbnail
	
		
	def checkMapName(self, name):
		
		if not 1 < len(name) < 15 or not name.isprintable():
			raise BadMapName()
		if not db.query(Map).filter_by(name = name).count() == 0:
			raise MapNameTaken()
  
	def to_json(self):
		print ("map to json")
		return {"mapId":self.id, "mapName":self.name, "turnsNum":self.turnsNum, "playersNum":self.playersNumber, "picture":self.picture}

	def __repr__(self):#потом подправить форматированый вывод
		return "<Map('%s' - , players Num '%s', turns Num'%s')>" % (self.name, self.playersNumber, self.turnsNum)


class Region(Base):
	__tablename__ = "regions"
	
	id = pkey()
	mapId = Column(Integer, ForeignKey('maps.id', onupdate='CASCADE', ondelete='CASCADE'),  primary_key=True)
	
	population = integer(True)
	
	#характеристики региона
	border = bool()
	coast = bool()
	mountain = bool()
	sea = bool()
	mine = bool()
	farmland = bool()
	magic = bool()
	forest = bool()
	hill = bool()
	swamp = bool()
	 
	
	def __init__(self, mapId, regNum, landDescription, adjacents, population=None):
		self.mapId = mapId
		self.id = regNum
		self.population = population
		
		for adj in adjacents:
			dbi.add(regionAdj(mapId, regionNum, adj))
		
	
	def __repr__(self):
		return "<Region(Map '%s', region '%s', adj'%s')>" % (self.mapId, self.regionNum, self.regionAdj)	

class RegionAdj(Base):
	__tablename__ = "region_adjacents"
	
	mapId = Column(Integer, ForeignKey('maps.id', onupdate='CASCADE', ondelete='CASCADE'),  primary_key=True)
	regionNum = Column(Integer, ForeignKey('regions.id', onupdate='CASCADE', ondelete='CASCADE'),  primary_key=True)
	regionAdj = pkey()
	
	def __init__(self, mapId, regionNum, regionAdj):
		self.mapId = mapId
		self.regionNum = regionNum  
		self.regionAdj = regionAdj
		
	def __repr__(self):
		return "<RegionAdj(Map '%s', region '%s', adj'%s')>" % (self.mapId, self.regionNum, self.regionAdj)	
	
class Game(Base):
	__tablename__ = "games"

	id = pkey()
	name = uniqstring() 
	mapId = fkey('maps.id')
	playersInGame = integer()
	gameStatus = integer()
	Description = string(True)
	turn = integer(True)
	activePlayerId=  integer(True)

	gameStatusWaiting = 1
	gameStatusProcessing = 2
	gameStatusEnd = 3

	def __init__(self, name, mapId, Description):
		if not db.checkMap(mapId):
			raise BadMapId()
			
		self.checkGameName(name)
		
		self.mapId = mapId  
		self.name = name
		self.gameStatus = self.gameStatusWaiting
		self.playersInGame = 0
		self.turn= 0
		self.Description = Description
   
	def checkGameName(self, name):
		if not 0 < len(name) < 50:
			raise BadGameName()
		if not db.query(Game).filter_by(name = name).count() == 0:
			raise GameNameTaken()

	def addPlayer(self):
		if self.playersInGame == self.getMaxPlayersInGame():
				raise TooManyPlayers()
		if self.gameStatus != self.gameStatusWaiting:
				raise BadGameState()
		self.playersInGame += 1
		
	def rmPlayer(self):
		self.playersInGame -= 1
		if self.playersInGame == 0:
			self.gameStatus = self.gameStatusEnd
		
	def getPlayers(self):
		if self.gameStatus != self.gameStatusEnd:
			return db.query(User).filter_by(gameId= self.id).all()

	def getMaxTurnInGame(self):
		return	db.query(Map).filter_by(id = self.mapId).one().turnsNum

	def getMaxPlayersInGame(self):
		return	db.query(Map).filter_by(id = self.mapId).one().playersNumber

	def updateStage(self):
		if self.gameStatus == self.gameStatusWaiting and len(self.getPlayers()) == len(db.query(User).filter_by(gameId= self.id, isReady = True).all()) and self.playersInGame == self.getMaxPlayersInGame():
			self.gameStatus = self.gameStatusProcessing


	def getStage(self):
		players = [{"username":user.name, "userId":user.id} for user in  db.query(User).filter_by(gameId = self.id).all()]
		stage = {"players":players}
		return stage

	def toList(self):
		print ("to list")
		create_list = lambda classAtr, restAtr, obj = self:	{ restAtr[i]: getattr(obj, classAtr[i]) for i in range(len(restAtr))}

		gameAttrs = ['id', 'name', 'Description', 'gameStatus', 'turn', 'activePlayerId', 'mapId']

		gameAttrNames = ['gameId', 'gameName', 'gameDescription', 'state',
			'turn', 'activePlayerId', 'mapId']

		print ("to sst")
		#gameDesr = {gameAttrNames[i] : getattr(self, gameAttrs[i]) for i in range(len(gameAttrs))}
		print ("end sst")
		gameDesr = create_list(gameAttrs, gameAttrNames)

		playerAttrs = ['id', 'name', 'isReady']
		playerAttrNames = ['userId', 'username', 'isReady']

		print ("players count - {0}".format(len(self.getPlayers())))
		gameDesr["players"] = [create_list(playerAttrs, playerAttrNames, pl) for pl in self.getPlayers()]


		gameDesr["turnsNum"] = self.getMaxTurnInGame()
		gameDesr["maxPlayersNum"] = self.getMaxPlayersInGame()

		return gameDesr
		return {}

	def __repr__(self):#потом подправить форматированый вывод
		return "<Game('%s','%s',)>" % (self.name, self.playersInGame)

class Chat(Base):
	__tablename__ = "chat"
	
	id = pkey()
	user = fkey('users.sid')
	message = string()
	time = integer()
	
	senderUser = relationship(User)
	
	def generateTimeForTest(self):
		db.lastTime = db.lastTime +1
		return db.lastTime

	def __init__(self, user, message):
		self.user = user
		self.message = message 
		self.time = math.trunc(time.time()) if not DEBUG else self.generateTimeForTest()
		if DEBUG:
			print ("time{0}".format(self.time));

class DataBase:
	instance = None
	lastSid = 0
	lastTime = 0 
	
	def __init__(self):
		self.db =  create_engine('sqlite:///:memory:', echo=False)
		Base.metadata.create_all(self.db)
		Session = sessionmaker(bind=self.db)
		self.session = Session()
		if (self.session == None):
			print("qqqq")
	
	def add(self, obj): 
		self.session.add(obj)
		self.commit()
		return None 
	
	def query(self, *args, **kwargs): 
		return self.session.query(*args,**kwargs)
	
	def commit(self): 
		self.session.commit()
	
	def rm(self, obj):
		self.session.delete(obj)
		self.commit()   

	def checkSid(self, sid):
		if self.query(User).filter_by(sid = sid).count() != 1:
			raise BadUserSid()

	def checkMap(self, mapId):
		return self.query(Map).filter_by(id = mapId).count() == 1 

	def getUser(self, sid):
		try:
			return self.query(User).filter_by(sid = sid).one()
		except exc.NoResultFound:
			raise BadUserSid()
	
	def getMessages(self, time, count):
		return self.query(Chat).filter(Chat.time > time).order_by(Chat.time).all()[-count:]

	def getGame(self, gameId):
		try:
			return self.query(Game).filter_by(id = gameId).one()
		except:
			raise BadGameId()

	def getMap(selp, mapId):
		try:
			return self.query(Map).filter_by(id = mapId).one()
		except sqlalchemy.orm.exc.NoResultFound:
			return False;
		
	def clear(self):
		if DEBUG:
			self.lastSid = 0
			self.lastTime = 0
		if DEBUG:
			print("clear sid {0} ".format(self.lastSid))
		for table in Base.metadata.sorted_tables:
			self.db.execute(table.delete())

db = DataBase()

