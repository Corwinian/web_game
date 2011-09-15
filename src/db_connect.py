'''
Created on 13.09.2011

@author: corwin
'''
import os
import sqlite3

from config import DB_CONFIG

class User:
    table_name = "users"
    name = None
    password = None
    
    def __init__(self, obj):
        self.name = obj[keys()[0]];
        self.password = obj[keys()[1]];
    
    def keys(self): #не смог придумать лучшего имени
        return ("key", "password")
    
    def values(self):
        return (self.name, self.password)
        
     
class Connected_User(User):
    table_name = "connected_users"
    sid = None

class DataBase:
    db = None
    
    def __init__(self ):
        create = not os.path.exists( DB_CONFIG["location"])
        self.db = sqlite3.connect( DB_CONFIG["location"])
        if create:
            cursor = self.db.cursor()
            cursor.execute("CREATE TABLE users ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                "user TEXT UNIQUE NOT NULL,"
                "password TEXT UNIQUE NOT NULL)")
            cursor.execute("CREATE TABLE connected_users ("
                "sid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                "user_id INTEGER NOT NULL, "
                "FOREIGN KEY (user_id) REFERENCES users)")
            self.db.commit()

    def checkUser(self, user):
        return
    def chechSID(self, sid):
        return
    def add(self, obj): # потом по нормальному занаследовать классы и повесить исключение
       
       cursor = self.db.cursor()
       cursor.execute("INSERT INTO ? (?) VALUES (?)", 
                      obj.table_name(), obj.keys(), obj.values())
       self.db.commit() 
    return

    def rm(db, user):
    return

data_Base = DataBase()
        