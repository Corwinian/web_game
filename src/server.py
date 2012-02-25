#!/usr/bin/python

import bottle
import sys
import parser

import json
import io

from config import DEBUG
from config import PORT
from config import SERVER 

DEBUG = False

@bottle.post('/') 
#//route('/')
def serve_ajax():
	ss = '''<form method="POST">
                <input name="name"     type="text" />
                <input name="password" type="password" />
              </form>'''
	return bottle.request.body

@bottle.post('/ajax') 
def serve_ajax():
	return parser.parse_request(bottle.request.body.read().decode("utf-8"))
	

def main():
	bottle.run(host=SERVER, port=PORT)
	return 0

if __name__ == '__main__':
    sys.exit(main())
