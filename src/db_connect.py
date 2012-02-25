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
			raise NotInGames()

		db.getGame(self.gameId).rmPlayer()
		
		self.gameId = None
		db.commit()

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
		
		
		if not  1 < playersNum < 5: 
			raise BadPlayersNum()
				
		if 5 > turnsNum > 10: 
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
   
	def __repr__(self):#потом подправить форматированый вывод
		return "<Map('%s','%s',)>" % (self.name, self.playersNumber)

class Game(Base):
	__tablename__ = "games"

	id = pkey()
	name = uniqstring() 
	mapId = fkey('maps.id')
	playersInGame = integer()
	gameStatus = string()
	Description = string(True)

	gameStatusWaiting = "waiting the begining"

	def __init__(self, name, mapId, Description):
		if not db.checkMap(mapId):
			raise BadMapId()
			
		self.checkGameName(name)
		
		self.mapId = mapId  
		self.name = name
		self.gameStatus = self.gameStatusWaiting
		self.playersInGame = 0
		self.Description = Description
		print(self.name)
   
	def checkGameName(self, name):
		if not 0 < len(name) < 50:
			raise BadGameName()
		if not db.query(Game).filter_by(name = name).count() == 0:
			raise GameNameTaken()

	def addPlayer(self):
		if self.playersInGame == self.getMaxPlayersInGame():
				raise TooManyPlayers()
		if self.gameStatus != self.gameStatusWaiting:
				raise TooManyPlayers()
		self.playersInGame += 1
		
	def rmPlayer(self):
		self.playersInGame -= 1
		
	def getMaxPlayersInGame(self):
		return	db.query(Map).filter_by(id = self.mapId).one().playersNumber

	def __repr__(self):#потом подправить форматированый вывод
		return "<Gae('%s','%s',)>" % (self.name, self.playersNumber)

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

