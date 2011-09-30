#!/usr/bin/python

import bottle
import sys
import parser

DEBUG = True
PORT = 8080
SERVER = '128.0.0.1'


@bottle.route('/')
def serve_ajax():
	return static_file('test.html')  

@bottle.route('/ajax')
def serve_ajax():
	if DEBUG: 
		print("request")
	return parse_request(request.GET['data'])

def main():
	bottle.run(host='127.0.0.1', port=PORT)
	return 0


if __name__ == '__main__':
    sys.exit(main())
