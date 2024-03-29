#!/usr/bin/python

import unittest

import os
import sys
import optparse
import json

from config import DEBUG
from config import JSON_DUMPS_FORMAT
from parser import parse_request

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
	print ("tese")
	result = list()
	if isinstance(object, list):
		for obj in object:
			print("obj")
			print(obj)
			result.append(json.loads(parse_request(obj)))
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

def parse_options():
	parser = optparse.OptionParser(usage='archivaor.py [begin] end [testCategory] ')
	parser.add_option('-g', '--group', dest='testGroup', help='compress metod', metavar='FILE', default= '')
	return parser.parse_args()

def main(a, b, c):
	global begin
	global end
	global testDir
	begin = a
	end = b
	testDir = c
	unittest.TextTestRunner().run(suite())

if __name__=='__main__':
	(options, args) = parse_options()

	DEF_DIR = "tests/"

	start = 0 if len(args)== 1 else int(args[0])
	fin = int(args[0 if len(args) == 1 else 1])
	directory = DEF_DIR + options.testGroup

	print (directory)
	main(start, fin, directory)
