#!/usr/bin/python
'''
Created on 11.09.2011

@author: corwin
'''
import json

from config import JSON_DUMPS_FORMAT


class RequestException(Exception):
	'''
    '''
	status = None
	message = None
	
	def __init__(self, status, message):
		self.status = status
		self.message = message
	
	def toJSON(self):
		json.dumps({"status":self.status, "message":self.message}, **JSON_DUMPS_FORMAT)

errors = ("NotComand", "BadCommand", "BadRequest", "BadNameOrPassword", "NotUser")

gen_exp = lambda name, status: type(name, (RequestException,), { "status": status })

for e in errors:
	globals()[e] = gen_exp(e,e)


