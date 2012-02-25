#!/usr/bin/python

import unittest

import os
import sys
import json

from config import DEBUG
from config import JSON_DUMPS_FORMAT
from parser import parse_request

DEF_DIR = "../tests/"

class TestFromFile(unittest.TestCase):
	def __init__(self, inFile, ansFile):
		super(TestFromFile, self).__init__()
		self.inFile = inFile
		self.ansFile = ansFile
		self.testDescr = ''
		self.maxDiff = None

	def tearDown(self):
		print ("Test %s description: %s\n" % (self.inFile, self.testDescr))
		
	def runTest(self):
		f = open(self.ansFile)
		ans = f.read()
		out = parseDataFromFile(self.inFile)
	
		self.testDescr = out['description']		
		self.assertListEqual(out['result'], json.loads(ans))
		
def parseDataFromFile(fileName):
	try:
		file = open(fileName, 'r')
	except:
		return 'Cannot open file %s' % fileName
	description = ''
	try:
		object = json.loads(file.read())
	except (TypeError, ValueError):
		return {'result': [{"result": "badJson"}], 'description': description}

	if not ('test' in object):
		return {'result': [{'result': 'badTest'}], 'description': description}

	if 'description' in object:
		description = object['description']
		
	object = object['test']			
	result = list()
	if isinstance(object, list):
		for obj in object:
			result.append(json.loads(parse_request(json.dumps(obj, **JSON_DUMPS_FORMAT))))
	else:
		result.append(parse_request(object))
		return {'result': [r1.read()], 'description': description}

	return {'result': result, 'description': description}		

def suite():
	suite = unittest.TestSuite()
	suite.addTests(TestFromFile('%s/test_%d.in' % (testDir, i), '%s/test_%d.ans' % (testDir, i)) for i in range(begin, end))
	return suite

def load_dirs(start_dir):
	return { dir : load_dirs(dir) for dir in os.listdir(start_dir) if os.path.isdir(dir)}

def help():
	sys.exit("Format: python TestFromFiles.py [testCategory [[begin] end | [-f road] ")		

def main(a, b, c):
	global begin
	global end
	global testDir	
	begin = a
	end = b
	testDir = c
	unittest.TextTestRunner().run(suite())

if __name__=='__main__':
	argc = len(sys.argv)
	
	directory =  (DEF_DIR + argv[1] if argc == 2  else DEF_DIR)
	
	if argc <= 2:
		fin = -1
		start = 0
		
	else if argc == 3:
		if sys.argv[1][0] != '-':
			directory = DEF_DIR + argv[1]
			fin = sys.argv[2]
		#TODO: add load one file
		#if sys.argv[1] == '-f':
		
	else:
		help()

			
	directory = DEF_DIR + argv[1]
	fin = int(sys.argv[1]) if argc == 2 else int(sys.argv[2])
	start =  int (sys.argv[1]) if argc >= 3 else 0
	directory = "../tests/" + (sys.argv[3] if argc == 4 else "protocol")
	main(start, fin, directory)
