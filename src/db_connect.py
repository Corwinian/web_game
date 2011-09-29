'''
Created on 13.09.2011

@author: corwin
'''
import os

from sqlalchemy import create_engine, Table, Boolean, Enum, Column, Integer, String, MetaData, Date, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from errors import *
from config import DB_CONFIG

Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	password = Column(String, nullable=False)
	sid = Column(String, nullable=True)
	
	def __init__(self, name, password):
		super().__init__()
		self.name = name;
		self.password = password;
	
	def setSid(self):
		self.sid = self.name + self.password
#		db.add(self)
		db.commit()
	
	def __repr__(self):
		return "<User('%s','%s',)>" % (self.name, self.password)

class Map(Base):
	__tablename__ = "maps"
	
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	playersNumber = Column(Integer, nullable=False)
	
	def __init__(self, name, playersNumber):
		super().__init__()
		self.name = name
		self.playersNumber = playersNumber
   
	def __repr__(self):#потом подправить форматированый вывод
		return "<User('%s','%s',)>" % (self.name, self.playersNumber)

class Game(Base):
	__tablename__ = "games"

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
#придумать могет сделать inique
	mapId = Column(Integer, ForeignKey('maps.id', onupdate='CASCADE', ondelete='CASCADE'))
	Description = Column(String, nullable=True)

	def __init__(self, name, mapId, Description):
		if not db.checkMap(mapId):
			raise BadMapId()
		if not self.checkGameName(name):
			raise BadGameName()
		self.mapId = mapId  
		self.name = name
		self.Description = Description
   
	def checkGameName(self, name):
		return 0 < len(name) < 50 or db.query(Game).filter_by(name = name).count() == 0

	def getMaxPlayersInGame(self):
		return	bd.query(Map).filter_by(id = self.mapId).one().playersNumber

	def __repr__(self):#потом подправить форматированый вывод
		return "<Gake('%s','%s',)>" % (self.name, self.playersNumber)

#may be move this to class User
class Player(Base):
	__tablename__ = "players"
	
	id = Column(Integer, primary_key=True)
	
	userId = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
	gameId = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
	
	def __init__(self, sid, gameId):
		userId = db.getUser(sid).id
		gameId = db.getGame(gameId).id		
	#проверить колическо активных игроков
#проверить не играет ли щас игрок
#проверить щас стутус игрыЪЪЪЪ
		
	def __repr__(self):
		return "<Player('%s','%s',)>" % (self.name, self.password)

class DataBase:
	#потом покуприть мануал и заменить на майскл
	instance = None

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
	

	def rm(self, object):
		self.session.delete(obj)
		self.commit()   

	def checkSid(self, sid):
		return self.query(User).filter_by(sid = sid).count() == 1 

	def checkMap(self, mapId):
		return self.query(Map).filter_by(id = mapId).count() == 1 

	def getUser(self, sid):
		try:
			return self.query(User).filter_by(id = sid).one()
		except:
			raise BadSid()

	def getGame(self, gameId):
		try:
			return self.query(Game).filter_by(id = gameId).one()
		except:
			raise BadGameId()

	def getMap(selp, mapId):
		try:
			return self.query(Map).filter_by(id = mapId).one()
		except:
			return False;
		
	def clear(self):
		for table in Base.metadata.sorted_tables:
#проверяем мап id	
			self.db.execute(table.delete())

db = DataBase()
