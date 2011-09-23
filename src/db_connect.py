'''
Created on 13.09.2011

@author: corwin
'''
import os

from sqlalchemy import create_engine, Table, Boolean, Enum, Column, Integer, String, MetaData, Date, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
	
	def genSid(self):
		self.sid = name+password
		return sel.sid  
	
	def __repr__(self):
		return "<User('%s','%s',)>" % (self.name, self.password)
   
   
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
	
	
	def query(self, *args, **kwargs): 
		return self.session.query(*args,**kwargs)
	

	def commit(self): 
		self.commit()
	

	def rm(self, object):
		self.session.delete(obj)
		self.commit()   

	def clear(self):
		for table in Base.metadata.sorted_tables:
			self.db.execute(table.delete())

db = DataBase()
