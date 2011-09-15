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
    __table_name__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    sid = Column(String, nullable=True)
    
    def __init__(self, name, password):
        self.name = name;
        self.password = password;
    
	def genSid()
		sid = name+password
		return sid  
    
	def __repr__(self):
       return "<User('%s','%s',)>" % (self.name, self.password)
   
   
class DataBase:
    #потом покуприть мануал и заменить на майскл
    db =  create_engine('sqlite:///:memory:', echo=True)
    session = sessionmaker(bind=db)
    
    def add(self, obj): # потом по нормальному занаследовать классы и повесить исключение
        self.session.add(obj)
        self.commit()
    return
    
    def query(self, obj): # потом по нормальному занаследовать классы и повесить исключение
        self.session.query(obj)
    return

    def commit(self): # потом по нормальному занаследовать классы и повесить исключение
        self.commit()
    return

    def rm(db, object):
        self.session.delete(obj)
        self.commit()
    return

data_Base = DataBase()
        
