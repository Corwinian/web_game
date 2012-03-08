#!/usr/bin/python

import bottle
import sys
import parser

import json
import io
import utils 
from config import DEBUG
from config import PORT
from config import SERVER 

DEBUG = True

STATIC_FILES_ROOT = utils.join("./client/")


@bottle.get('/') 
def serve_main():
	if DEBUG:
		print ("Root dir {0}".format(STATIC_FILES_ROOT))
	return bottle.static_file('main.html', STATIC_FILES_ROOT)

@bottle.route('/:root#css.*|images.*|js.*#/:filename')
def serve_dirs(root,filename):
	return bottle.static_file(filename, utils.join(STATIC_FILES_ROOT, root))

@bottle.route('/:filename#.*\.css#')
@bottle.route('/:filename#.*\.ico#')
@bottle.route('/:filename#.*\.js#')
def serve_root_statics(filename):
	return bottle.static_file(filename, STATIC_FILES_ROOT)


@bottle.get('/ajax') 
def serve_ajax():
	if DEBUG:
		print ("Post query")
		#req = json.loads(request.GET['data'])

#	return parser.parse_request(bottle.request.body.read().decode("utf-8"))
	return parser.parse_request(json.loads(bottle.request.GET['data']))
	

def main():
	bottle.run(host=SERVER, port=PORT)
	return 0

if __name__ == '__main__':
    sys.exit(main())
