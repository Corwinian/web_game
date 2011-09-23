#!/usr/bin/python
'''
Created on 11.09.2011

@author: corwin
'''

errors = (
	"badAction", 
	"badJson", 
	"badUsername",
	"badPassword", 
	"usernameTaken", 
	"badUsernameOrPassword", 
	"userLoggedIn", 
	"badSid")

class RequestException(Exception):
	'''
    '''
	def __init__(self, message = None):
		self.message = message
	
	def toDict(self):
		return {"result" : self.result} if self.message != None else {"result" : self.result, "message" : self.message} 


for e in errors:
	name = e[0].upper() + e[1:]
	globals()[name] =  type(name, (RequestException,), { "result": e })


